# About lammps-logfile

`lammps-logfile` is a lightweight package for reading time-series data from LAMMPS log files.

Basic usage to get and plot the temperature in a simulation as a function of time is:

```python
import lammps_logfile
import matplotlib.pyplot as plt

# Read the log file into a pandas DataFrame
data = lammps_logfile.read_log("log.lammps")

x = data["Time"]
y = data["Temp"]

plt.plot(x, y)
plt.show()
```
