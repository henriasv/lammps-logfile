from io import StringIO
import pandas as pd

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

def read_log(filename):
    """
    Reads a LAMMPS log file and returns a pandas DataFrame containing all thermo data.

    This function parses the log file, extracting all thermodynamic output blocks (thermo data).
    It concatenates data from multiple runs into a single DataFrame, adding a 'run_num' column
    to distinguish between them. It handles varying columns between runs by filling missing
    data with NaNs (pandas default behavior).

    Parameters
    ----------
    filename : str or file-like object
        Path to the LAMMPS log file or a file-like object.

    Returns
    -------
    pd.DataFrame
        DataFrame containing all thermo data from the log file.
    """

    start_thermo_strings = ["Memory usage per processor", "Per MPI rank memory allocation"]
    stop_thermo_strings = ["Loop time", "ERROR", "Fix halt condition"]

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

    while i < len(contents):
        line = contents[i]

        if keyword_flag:
            block_lines = []
            # Capture the block until a stop string is found
            while i < len(contents):
                line = contents[i]
                if any(s in line for s in stop_thermo_strings):
                    break
                block_lines.append(line)
                i += 1

            # Parse the captured block
            tmp_string = "".join(block_lines)
            if tmp_string.strip():
                # Check for multi style (heuristic: Look for the separator line)
                if "------------ Step" in tmp_string:
                    df = _parse_multi_style(block_lines)
                    if not df.empty:
                        df['run_num'] = run_num
                        dfs.append(df)
                        run_num += 1
                else:
                    try:
                        # pandas read_csv with whitespace separator
                        df = pd.read_csv(StringIO(tmp_string), sep=r'\s+')
                        if not df.empty:
                            df['run_num'] = run_num
                            dfs.append(df)
                            run_num += 1
                    except pd.errors.EmptyDataError:
                        pass

            keyword_flag = False
            # Don't increment i here, we want to process the stop line (though usually it just ends the block)
            continue

        # Check for start strings
        if any(line.startswith(s) for s in start_thermo_strings):
            keyword_flag = True

        i += 1

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)
