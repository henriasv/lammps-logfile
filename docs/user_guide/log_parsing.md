# Log Parsing Details

`lammps-logfile` is designed to be robust against the variability of LAMMPS log files.

## Run Styles

LAMMPS allows for different `thermo_style` settings (e.g., `one`, `multi`, `custom`).

*   **Custom**: The parser reads the header line (e.g., `Step Temp Press`) to identify columns.
*   **Multi**: The parser detects the `------------ Step` separator and parses the following lines.
*   **Mixed**: If a log file switches styles between runs, `read_log` attempts to unify the data. If columns are missing in some runs, they may be filled with NaN or handled according to pandas concatenation rules.

## Performance Optimization

For `thermo_style multi`, the parser checks for the separator string within the first 10 lines of a block to avoid scanning the entire file unnecessarily. This ensures efficient processing even for large files.

## Multiple Runs

When a log file contains multiple `run` commands, the output from each is parsed and concatenated.

*   A `run_num` column is automatically added to the DataFrame.
*   `run_num` starts at 0 for the first run found in the file.
