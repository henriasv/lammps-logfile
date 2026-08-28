# Pro Tips: Advanced Analysis

Since `read_log` returns a standard Pandas DataFrame, you can leverage the full power of the PyData ecosystem. Here are some advanced patterns for analyzing your simulation data.

## Filtering by Run Number

If your log file contains multiple runs (e.g., equilibration followed by production), they are distinguished by the `run_num` column.

```python
import lammps_logfile

df = lammps_logfile.read_log("log.lammps")

# Select only the production run (e.g., run_num 1)
production_data = df[df['run_num'] == 1]
```

## Calculating Running Averages

Smooth noisy thermodynamic data using Pandas' rolling window functions:

```python
# Calculate a 100-step rolling average of Temperature
df['Temp_Smooth'] = df['Temp'].rolling(window=100).mean()

# Plot raw vs smooth
import matplotlib.pyplot as plt
plt.plot(df['Step'], df['Temp'], alpha=0.3, label='Raw')
plt.plot(df['Step'], df['Temp_Smooth'], color='red', label='Smoothed')
plt.legend()
plt.show()
```

## Resampling Time-Series Data

If you have valid time units, you can convert the index to a datetime or timedelta index for powerful resampling.

```python
import pandas as pd

# Assuming timestep is 1 femtosecond, create a time index
df['Time'] = pd.to_timedelta(df['Step'] * 1e-15, unit='s')
df = df.set_index('Time')

# Resample to 1-picosecond intervals, taking the mean
resampled_df = df.resample('1ps').mean()
```

## Exporting for Other Tools

You can easily export your data to other formats:

```python
# Save as CSV
df.to_csv("simulation_data.csv", index=False)

# Save as Excel
df.to_excel("simulation_data.xlsx")

# Save to HDF5 (fast and efficient for large data)
df.to_hdf("simulation_data.h5", key="lammps")
```
