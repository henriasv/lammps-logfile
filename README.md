# Lammps logfile reader
Tool to read a lammps logfile into a reasonable python data structure.

## Basic usage

```
log = lammps_logfile.File("path/to/logfile")

x = log.get("Time")
y = log.get("Temp")

plt.plot(x, y)
```
This will give the concatenated log entries of all the runs where the thermo output didn't change with respect to the last run. I.e. if the entries in the `thermo_style` was not changed between runs it will contain the log data for all the timesteps. If the `thermo_style` *was* changed, `x` and `y` will contain the data from all the timesteps after the `thermo_style` was changed for the last time. 
 
## Multiple runs in the same log file
If multiple run statements have been made in a simulation, these can be retrieved bu supplying the `run_num` keyword to the `get()`-function

```
log = lammps_logfile.File("path/to/logfile")

x = log.get("Time", run_num=N)
y = log.get("Temp", run_num=N)

plt.plot(x, y)
```
In this case, `x` and `y` will contain the log data from the `N`'th `run` command in LAMMPS, counting from 0.
