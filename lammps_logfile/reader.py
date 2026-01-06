from io import StringIO

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
    import pandas as pd

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
