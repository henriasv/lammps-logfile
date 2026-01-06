![](https://github.com/henriasv/lammps-logfile/workflows/Install%20and%20tests/badge.svg)
# LAMMPS logfile reader
Tool to read a logfile produced by [LAMMPS](https://lammps.sandia.gov) into a python data structure.

## Installation
From pypi (preferred/stable)
```
pip install lammps-logfile
```
Depending on your python installation, you may have to use `pip3` instead of `pip`. This is usualy the case if you need to run `python3` rather than `python` to run python version 3. 

Install using pip directly from github to get the latest (possibly unstable) version:
```
pip install git+https://github.com/henriasv/lammps-logfile.git
```
Or by cloning the repository:
```
git clone https://github.com/henriasv/lammps-logfile.git
cd lammps-logfile
pip3 install .
```

## Usage (Recommended)
The recommended way to read log files is using the `read_log` function, which returns a pandas DataFrame containing all thermodynamic data from all runs in the log file.

```python
from lammps_logfile import read_log
import matplotlib.pyplot as plt

# Read the log file into a DataFrame
# This example uses the 'crack_log.lammps' file found in 'examples/logfiles/'
df = read_log("crack_log.lammps")

# The DataFrame contains data from all runs, with a 'run_num' column distinguishing them
print(df.head())

# Plot Temperature vs Step
plt.figure(figsize=(10, 6))
plt.plot(df['Step'], df['Temp'])
plt.xlabel('Step')
plt.ylabel('Temperature')
plt.show()
```

![Example Plot](docs/readme_example.png)

## Benchmarks

The following benchmarks demonstrate the performance of `read_log` on various log files (including those with mixed `thermo_style` outputs). The benchmarks were run on the provided examples.

| Simulation                              |   Runs |   Steps |   Memory (MB) |   Time (s) |
|:----------------------------------------|-------:|--------:|--------------:|-----------:|
| 01_fcc_thermo_multi/out/log.lammps      |      3 |      29 |          0.10 |     0.02   |
| 02_bcc_custom_thermo/out/log.lammps     |      4 |     108 |          0.15 |     0.02   |
| 03_fcc_custom_longlog/out/log.lammps    |      4 |   30004 |         21.77 |     0.74   |
| 04_bcc_multi_then_custom/out/log.lammps |      5 |      62 |          0.16 |     0.03   |

## Legacy Interface
The `File` class interface is kept for backward compatibility but is considered legacy.

```python
import lammps_logfile

log = lammps_logfile.File("path/to/logfile")

x = log.get("Time")
y = log.get("Temp")

import matplotlib.pyplot as plt
plt.plot(x, y)
plt.show()
```
This will give the concatenated log entries of all the runs where the style of the thermo output didn't change with respect to the last run. I.e. if the entries in the `thermo_style` was not changed between runs it will contain the log data for all the timesteps. If the `thermo_style` *was* changed, `x` and `y` will contain the data from all the timesteps after the `thermo_style` was changed for the last time. 
 
### Multiple runs in the same log file (Legacy)
If multiple run statements have been made in a simulation, these can be retrieved bu supplying the `run_num` keyword to the `get()`-function

```python
import lammps_logfile

log = lammps_logfile.File("path/to/logfile")

x = log.get("Time", run_num=N)
y = log.get("Temp", run_num=N)

import matplotlib.pyplot as plt
plt.plot(x, y)
plt.show()
```
In this case, `x` and `y` will contain the log data from the `N`'th `run` command in LAMMPS, counting from 0.

Any invalid call to the `get()`-function will result in the function returning `None`. This happes if the user asks for a thermo propery that does not exist in the log file, or if the user asks for a `run_num` larger than the number of runs in the logfile. 
