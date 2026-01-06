"""
Running Average
===============

This example shows how to calculate and plot a running average of a property (Temperature)
from a LAMMPS log file.
"""

import matplotlib.pyplot as plt
import lammps_logfile
import os
import pandas as pd

# Path to the example log file
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

candidate_path = os.path.abspath(os.path.join(script_dir, "../../examples/logfiles/crack_log.lammps"))

log_path = candidate_path

# Read the log file
data = lammps_logfile.read_log(log_path)

# Calculate a rolling average (window size of 50 steps for demonstration)
# Note: The window size depends on your data frequency and noise.
window_size = 5
data['Temp_Rolling'] = data['Temp'].rolling(window=window_size).mean()

# Plot raw data vs rolling average
plt.figure(figsize=(10, 6))
plt.plot(data['Step'], data['Temp'], label='Raw Temperature', alpha=0.5)
plt.plot(data['Step'], data['Temp_Rolling'], label=f'Running Avg (Window={window_size})', linewidth=2)

plt.xlabel('Step')
plt.ylabel('Temperature (K)')
plt.title('Temperature with Running Average')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
