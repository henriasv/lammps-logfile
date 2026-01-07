# Log Parsing Details

This document explains the internal implementation of `lammps-logfile`'s parsing logic. It is useful for developers who want to contribute to the core reader or understand the performance characteristics.

## Implementation Overview

The parsing logic (found in `lammps_logfile.reader.read_log`) uses a block-based approach to handle the variability of LAMMPS log files. Instead of assuming a fixed structure, it scans the file for specific "start" and "stop" keywords that delineate thermodynamic data blocks (the output of a `run` command).

### Block Detection

The detection of a valid run block relies on recognizing start strings typical of LAMMPS output:

```python
start_strings = [
    "Memory usage per processor",
    "Per MPI rank memory allocation"
]
```

When one of these strings is encountered, the parser enters a "capture mode". It collects lines until a stop string is found:

```python
stop_strings = [
    "Loop time",
    "ERROR",
    "Fix halt condition"
]
```

This robustly isolates the thermodynamic data from other log output (e.g., potential energy initialization, neighbor list builds).

## Handling Run Styles

LAMMPS allows for different `thermo_style` settings, which produce different output formats. `lammps-logfile` automatically detects and handles these.

### `thermo_style custom` (Default)

In the `custom` style (or `one`), the data is preceded by a header line containing the column names (e.g., `Step Temp Press`).

*   **Logic**: The parser accumulates the block lines and passes them to `pandas.read_csv` using the C-based engine.
*   **Separator**: Since LAMMPS uses whitespace, `sep=r'\s+'` is used.

### `thermo_style multi`

In the `multi` style, data is output across multiple lines per timestep, separated by a header:
```text
------------ Step 0 ----- CPU = 0.0000 (sec) -------------
TotEng   = -5.2737        KinEng   = 1.4996
...
```

*   **Detection**: The parser checks the first 10 lines of a captured block. If a line starts with `------------ Step`, it identifies the block as `multi` style.
*   **Parsing**: A specialized function `_parse_multi_style` iterates through the lines. It extracts the `Step` and `CPU` from the separator line and parses the following `Key = Value` pairs into a dictionary for that timestep.

## Performance Optimization
Parsing large text files requires careful optimization. `lammps-logfile` achieves **>100 MB/s** effective parsing speeds through:

1.  **Memory-Mapped Scanning**: The library uses `mmap` to scan the file for data blocks directly on disk, avoiding the need to load the entire text file into Python memory.
2.  **Zero-Copy Slicing**: Identified data blocks are passed as memory views directly to `pandas.read_csv`, minimizing data copying.
3.  **Pandas C-Engine**: The heavy numeric parsing is handled by the optimized Pandas C-backend.

> [!NOTE]
> **Minimal Memory Footprint**: Unlike naïve parsers that read the whole file (`readlines()`), this implementation's memory usage is primarily determined by the size of the *output* data, not the input text file.

## Completeness & Accuracy

*   **Multiple Runs**: The parser maintains a `run_num` counter. Each successfully parsed block increments this counter and receives a `run_num` column. The blocks are then concatenated into a single DataFrame.
*   **Missing Columns**: If a log file switches `thermo_style` between runs (e.g., adding a new compute), the final DataFrame will contain the union of all columns. Timesteps where a column was not present will have `NaN` values, ensuring no data is discarded.
