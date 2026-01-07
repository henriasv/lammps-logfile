import pandas as pd
import mmap
import io
import os

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
                    if "CPU" in parts:
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

def _read_log_mmap(filename):
    """
    Optimized reader using memory mapping for large files.
    """
    if isinstance(filename, str):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} not found.")
        filepath = filename
        f = open(filename, "rb")
        own_handle = True
    elif hasattr(filename, "fileno"):
        # File object with file descriptor
        f = filename
        own_handle = False
        try:
           # Reset pointer
           f.seek(0)
        except Exception:
           pass
    else:
        # Cannot mmap
        return None

    try:
        # Check if file is empty
        try:
            if os.fstat(f.fileno()).st_size == 0:
                 if own_handle: f.close()
                 return pd.DataFrame()
        except Exception:
            # Fallback if fstat fails
            pass

        try:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        except ValueError:
             # Can happen for empty files or special files
             if own_handle: f.close()
             return pd.DataFrame()

        dfs = []
        run_num = 0
        
        # Bytes markers
        START_MARKERS = [b"Memory usage per processor", b"Per MPI rank memory allocation"]
        STOP_MARKERS = [b"Loop time", b"ERROR", b"Fix halt condition"]
        
        pos = 0
        size = mm.size()
        
        while pos < size:
            # Find earliest start marker
            start_idx = -1
            
            for m in START_MARKERS:
                idx = mm.find(m, pos)
                if idx != -1:
                    if start_idx == -1 or idx < start_idx:
                        start_idx = idx
            
            if start_idx == -1:
                break
            
            # Find end of the marker line to start capturing data
            eol = mm.find(b"\n", start_idx)
            if eol == -1:
                break
            
            current_scan_pos = eol + 1
            
            # Find earliest stop marker
            stop_idx = -1
            
            for m in STOP_MARKERS:
                idx = mm.find(m, current_scan_pos)
                if idx != -1:
                    if stop_idx == -1 or idx < stop_idx:
                        stop_idx = idx
            
            if stop_idx == -1:
                stop_idx = size
            
            # Extract block
            block_bytes = mm[current_scan_pos:stop_idx]
            
            # Check for multi style in header (first 1000 bytes)
            head_check = block_bytes[:1000]
            is_multi = b"------------ Step" in head_check

            if is_multi:
                # Decode and parse multi style
                block_str = block_bytes.decode('utf-8', errors='replace')
                df = _parse_multi_style(block_str.splitlines())
                if not df.empty:
                    df['run_num'] = run_num
                    dfs.append(df)
                    run_num += 1
            else:
                # Custom style
                if block_bytes.strip():
                    try:
                        # Use pandas C engine directly on bytes
                        df = pd.read_csv(io.BytesIO(block_bytes), sep=r'\s+', engine='c')
                        if not df.empty:
                            df['run_num'] = run_num
                            dfs.append(df)
                            run_num += 1
                    except pd.errors.EmptyDataError:
                        pass
                    except Exception:
                        pass

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
                if "Loop time" in line or "ERROR" in line or "Fix halt condition" in line:
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
                    if not df.empty:
                        df['run_num'] = run_num
                        dfs.append(df)
                        run_num += 1
                else:
                    tmp_string = "".join(block_lines)
                    if tmp_string.strip():
                        try:
                            df = pd.read_csv(io.StringIO(tmp_string), sep=r'\s+')
                            if not df.empty:
                                df['run_num'] = run_num
                                dfs.append(df)
                                run_num += 1
                        except pd.errors.EmptyDataError:
                            pass

            keyword_flag = False
            continue

        if line.startswith("Memory usage per processor") or line.startswith("Per MPI rank memory allocation"):
            keyword_flag = True

        i += 1

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)

def read_log(filename):
    """
    Reads a LAMMPS log file and returns a pandas DataFrame containing all thermo data.
    
    Now attempts to use fast mmap-based parsing, falling back to robust line-based parsing
    for streams or unsupported file objects.
    """
    # Try mmap optimized reader first
    try:
        df = _read_log_mmap(filename)
        if df is not None:
             return df
    except Exception:
        pass # Fallback
        
    # use legacy
    return _read_log_legacy(filename)
