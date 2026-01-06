# Getting started

## Getting log data

```python
import lammps_logfile
data = lammps_logfile.read_log("path/to/log.lammps")
```

The `read_log` function returns a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) containing the thermodynamic data from the log file. If the log file contains multiple runs, they are concatenated into a single DataFrame with a `run_num` column distinguishing them.

```python
t = data["Time"]
temp = data["Temp"]
```

Now `t` and `temp` are pandas Series containing the data for the `Time` and `Temp` columns.

## Plotting log data

```{literalinclude} python/getting_started.py
:lines: 11-16
```

To make the plot pop up in a window rather than being saved to a file, run `plt.show()` rather than `plt.savefig(...)`.

```{figure} python/time_temp.png
:scale: 100 %
:alt: Plot of temperature vs. time

Plot of temperature vs. time
```

## Running average

Since the data is in a pandas DataFrame, we can easily calculate running averages using pandas built-in methods:

```{literalinclude} python/getting_started.py
:lines: 20-29
```

```{figure} python/time_temp_avg.png
:scale: 100 %
:alt: Plot of temperature vs. time

Plot of temperature vs. time. The blue curve is the raw output, whereas in the orange curve the temperature has been smoothed over a 100 log entries wide averaging window.
```

## What data are available in the log file?

To inspect what columns are available, you can print the columns of the DataFrame:

```python
print(data.columns.tolist())
```

This will output a list of available column names, for example:

```{literalinclude} python/output.txt
```

## Command line tool

The following is the help message from the command line tool `lammps_logplotter` that comes with lammps-logplotter. This tool is meant to quicky inspect lammps log files without having to write a python script.

```bash
usage: lammps_logplotter [-h] [-x X] [-y Y [Y ...]] [-a RUNNING_AVERAGE] input_file

Plot contents from lammps log files

positional arguments:
  input_file            Lammps log file containing thermo output from lammps simulation.

optional arguments:
  -h, --help            show this help message and exit
  -x X                  Data to plot on the first axis
  -y Y [Y ...]          Data to plot on the second axis. You can supply several names to get several plot lines in the same figure.
  -a RUNNING_AVERAGE, --running_average RUNNING_AVERAGE
                        Optionally average over this many log entries with a running average. Some thermo properties fluctuate wildly, and often we are interested in te
                        running average of properties like temperature and pressure.
```
