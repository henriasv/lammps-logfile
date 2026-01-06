# Quickstart

This guide will get you up and running with `lammps-logfile` in less than 30 seconds.

## Reading a Log File

The primary interface is `lammps_logfile.read_log`. It parses the log file and returns a pandas DataFrame.

```python
import lammps_logfile

# Assuming you have a 'log.lammps' file
df = lammps_logfile.read_log("log.lammps")

# Inspect the data
print(df.head())
```

## Plotting Data

Since the data is a standard pandas DataFrame, you can use any plotting library you prefer, such as `matplotlib` or `seaborn`.

```python
import matplotlib.pyplot as plt

plt.figure()
plt.plot(df['Step'], df['Temp'])
plt.xlabel('Simulation Step')
plt.ylabel('Temperature')
plt.show()
```

## Handling Multiple Runs

If your log file contains multiple `run` commands, `read_log` concatenates them into a single DataFrame by default. A `run_num` column is added to distinguish between different run sections.

```python
# Filter for a specific run
run_0_data = df[df['run_num'] == 0]
```
