# Command Line Interface

`lammps-logfile` provides a command-line tool `lammps_logplotter` for quickly visualizing log files without writing Python code.

## Basic Usage

To plot two variables against each other:

```bash
lammps_logplotter log.lammps -x Step -y Temp
```

## Options

- **`-x`, `--xaxis`**: Variable to use for the X-axis (default: `Step`).
- **`-y`, `--yaxis`**: Variable(s) to use for the Y-axis. You can specify multiple variables (e.g., `-y Temp Press`).
- **`-s`, `--save`**: Save the plot to a file instead of showing it (e.g., `-s plot.png`).
- **`--csv`**: Save the parsed data to a CSV file (e.g., `--csv data.csv`).

## Examples

**Plot Temperature and Pressure vs Time:**

```bash
lammps_logplotter log.lammps -x Time -y Temp Press
```

**Save data to CSV for external analysis:**

```bash
lammps_logplotter log.lammps --csv simulation_data.csv
```
