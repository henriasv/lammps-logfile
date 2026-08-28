import pandas as pd
import mmap
import io
import os

# A thermo block starts on the line after one of these markers.
START_MARKERS = ["Memory usage per processor", "Per MPI rank memory allocation"]

# A thermo block ends at the first line containing one of these markers, or at
# the next START_MARKER (a new run), or at end of file -- whichever comes first.
# "Total wall time" is printed by LAMMPS at exit and is the only terminator for
# a run that never printed its "Loop time" summary.
STOP_MARKERS = ["Loop time", "ERROR", "Fix halt condition", "Total wall time"]


def _is_start_line(line):
    return any(line.startswith(m) for m in START_MARKERS)


def _is_stop_line(line):
    return any(m in line for m in STOP_MARKERS)


def _is_numeric_row(line, n_cols):
    """True if `line` consists of exactly `n_cols` whitespace-separated numbers."""
    tokens = line.split()
    if len(tokens) != n_cols:
        return False
    try:
        for t in tokens:
            float(t)
    except ValueError:
        return False
    return True


def _parse_custom_block(block):
    """
    Parse a `thermo_style custom`/`one` block (a header line followed by rows
    of numbers) into a DataFrame. `block` may be str or bytes.

    Fast path: hand the whole block to pandas' C engine. If the result has a
    non-numeric column, or pandas cannot parse the block at all, the block
    contained lines that are not thermo rows (e.g. trailing output from a run
    that never printed "Loop time", or a WARNING printed mid-run). In that case
    re-parse keeping only the header and the lines that are pure numeric rows.
    """
    buf = io.BytesIO(block) if isinstance(block, bytes) else io.StringIO(block)
    try:
        df = pd.read_csv(buf, sep=r'\s+', engine='c')
        if all(pd.api.types.is_numeric_dtype(dt) for dt in df.dtypes):
            return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
    except pd.errors.ParserError:
        pass

    text = block.decode('utf-8', errors='replace') if isinstance(block, bytes) else block
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return pd.DataFrame()
    header = lines[0]
    n_cols = len(header.split())
    rows = [l for l in lines[1:] if _is_numeric_row(l, n_cols)]
    return pd.read_csv(io.StringIO("\n".join([header] + rows) + "\n"), sep=r'\s+', engine='c')


def _parse_multi_style(lines):
    """
    Parses a block of lines in LAMMPS 'thermo_style multi' format.
    Returns a pandas DataFrame.
    """
    data = []
    current_step = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("------------ Step"):
            # If we have collected data for a step (and it's not empty), append it
            if current_step:
                data.append(current_step)
            current_step = {}

            # Parse the header line
            # Format: ------------ Step <step> ----- CPU = <cpu> (sec) -------------
            clean_line = line.replace("-", " ")
            parts = clean_line.split()

            if "Step" in parts:
                try:
                    step_idx = parts.index("Step") + 1
                    current_step["Step"] = int(parts[step_idx])
                except (ValueError, IndexError):
                    pass

            if "CPU" in parts:
                try:
                    # CPU = <val>
                    cpu_idx = parts.index("CPU") + 2 # Skip '='
                    if cpu_idx < len(parts):
                         current_step["CPU"] = float(parts[cpu_idx])
                except (ValueError, IndexError):
                    pass

        elif "=" in line:
            # Parse Key = Value pairs
            # Example: TotEng = -5.2737 KinEng = 1.4996
            parts = line.split()
            # Iterate in chunks of 3: Key, =, Value
            i = 0
            while i + 2 < len(parts):
                if parts[i+1] == "=":
                    key = parts[i]
                    try:
                        value = float(parts[i+2])
                        current_step[key] = value
                    except ValueError:
                        pass
                    i += 3
                else:
                    # In case parsing gets out of sync, advance 1
                    i += 1

    # Append the last step if exists
    if current_step:
        data.append(current_step)

    return pd.DataFrame(data)


class _MarkerFinder:
    """
    Finds the earliest occurrence of any of a set of byte markers at or after a
    position in an mmap, remembering the next occurrence of each marker so that
    a marker absent from the rest of the file is not re-scanned for every block.
    """
    def __init__(self, mm, markers):
        self.mm = mm
        self.markers = markers
        self._next = {}  # marker -> next known index (>= last query), or None if absent

    def earliest(self, pos):
        best = -1
        for m in self.markers:
            idx = self._next.get(m, -1)
            if idx is None:
                continue
            if idx < pos:
                idx = self.mm.find(m, pos)
                self._next[m] = None if idx == -1 else idx
                if idx == -1:
                    continue
            if best == -1 or idx < best:
                best = idx
        return best


def _read_log_mmap(filename):
    """
    Optimized reader using memory mapping for large files.
    Returns None if the input cannot be memory-mapped (caller falls back).
    """
    if isinstance(filename, str):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} not found.")
        f = open(filename, "rb")
        own_handle = True
    elif hasattr(filename, "fileno"):
        f = filename
        own_handle = False
        try:
            f.fileno()
            f.seek(0)
        except (OSError, ValueError):
            # io.UnsupportedOperation (StringIO/BytesIO etc.): cannot mmap.
            return None
    else:
        return None

    try:
        try:
            if os.fstat(f.fileno()).st_size == 0:
                if own_handle: f.close()
                return pd.DataFrame()
        except OSError:
            pass

        try:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        except (OSError, ValueError):
            # Special files etc.: let the line-based reader handle it.
            if own_handle: f.close()
            return None

        dfs = []
        run_num = 0

        start_finder = _MarkerFinder(mm, [m.encode() for m in START_MARKERS])
        stop_finder = _MarkerFinder(mm, [m.encode() for m in STOP_MARKERS])

        pos = 0
        size = mm.size()

        while pos < size:
            start_idx = start_finder.earliest(pos)
            if start_idx == -1:
                break

            # Data starts on the line after the start marker
            eol = mm.find(b"\n", start_idx)
            if eol == -1:
                break
            current_scan_pos = eol + 1

            # Block ends at the earliest stop marker or the next run's start
            # marker (for runs that never printed "Loop time"), else at EOF.
            stop_idx = stop_finder.earliest(current_scan_pos)
            next_start_idx = start_finder.earliest(current_scan_pos)
            if next_start_idx != -1 and (stop_idx == -1 or next_start_idx < stop_idx):
                stop_idx = next_start_idx
            if stop_idx == -1:
                stop_idx = size

            block_bytes = mm[current_scan_pos:stop_idx]

            # Check for multi style in header (first 1000 bytes)
            is_multi = b"------------ Step" in block_bytes[:1000]

            if is_multi:
                block_str = block_bytes.decode('utf-8', errors='replace')
                df = _parse_multi_style(block_str.splitlines())
            elif block_bytes.strip():
                df = _parse_custom_block(block_bytes)
            else:
                df = pd.DataFrame()

            if not df.empty:
                df['run_num'] = run_num
                dfs.append(df)
                run_num += 1

            pos = stop_idx

        mm.close()
        if own_handle:
            f.close()

        if not dfs:
            return pd.DataFrame()
        return pd.concat(dfs, ignore_index=True)

    except Exception:
        if own_handle:
            f.close()
        return None # Fallback


def _read_log_legacy(filename):
    """
    Legacy line-based parser for file-like objects (StringIO etc).
    """
    if hasattr(filename, "read"):
        logfile = filename
        close_file = False
    else:
        logfile = open(filename, 'r')
        close_file = True

    try:
        contents = logfile.readlines()
    finally:
        if close_file:
            logfile.close()

    dfs = []
    keyword_flag = False
    run_num = 0
    i = 0
    n_lines = len(contents)

    while i < n_lines:
        line = contents[i]

        if keyword_flag:
            block_lines = []
            while i < n_lines:
                line = contents[i]
                # A block also ends where the next run starts, for runs that
                # never printed "Loop time".
                if _is_stop_line(line) or _is_start_line(line):
                    break
                block_lines.append(line)
                i += 1

            if block_lines:
                is_multi = False
                for j in range(min(10, len(block_lines))):
                     if block_lines[j].strip().startswith("------------ Step"):
                         is_multi = True
                         break

                if is_multi:
                    df = _parse_multi_style(block_lines)
                else:
                    df = _parse_custom_block("".join(block_lines))

                if not df.empty:
                    df['run_num'] = run_num
                    dfs.append(df)
                    run_num += 1

            keyword_flag = False
            continue

        if _is_start_line(line):
            keyword_flag = True

        i += 1

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)


def read_log(filename):
    """
    Reads a LAMMPS log file and returns a pandas DataFrame containing all thermo data.

    Attempts fast mmap-based parsing first, falling back to line-based parsing
    for streams (e.g. StringIO) or unsupported file objects.
    """
    try:
        df = _read_log_mmap(filename)
        if df is not None:
             return df
    except Exception:
        pass # Fallback

    return _read_log_legacy(filename)
