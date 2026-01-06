"""
Basic Plotting
==============

This example demonstrates how to read a LAMMPS log file and plot Temperature vs Step.
"""

import matplotlib.pyplot as plt
import lammps_logfile
import os

# We use the included example file 'crack_log.lammps'
# In a real scenario, you would provide the path to your own log file.
# The path is relative to the execution of this script.
# We need to find the absolute path to the example file because sphinx-gallery runs in a different directory

# Locate the examples directory relative to the repository root
# This assumes the script is running from the docs/examples/ directory
# but we need to find the repo root.
# A safe way in this dev environment is to use the absolute path we know or search for it.
# In the build environment, `__file__` might be tricky with sphinx-gallery.
# However, sphinx-gallery executes the script, so `__file__` should be the path to the script being executed.

# Let's try to find the repo root by going up from the current working directory
# or using a hardcoded relative path if we know where we run.
# Sphinx-gallery runs in `docs/examples` (target dir).

# But wait, sphinx-gallery usually copies files.
# Let's assume we are in the gallery execution directory.
# The original file is in `examples/logfiles/crack_log.lammps` relative to repo root.
# Let's try to locate it.

try:
    # Try finding it relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # If __file__ is not defined (e.g. some execution contexts), use CWD
    script_dir = os.getcwd()

# Search for the file
# We expect to be in docs/examples or similar. Repo root is ../../
candidate_path = os.path.abspath(os.path.join(script_dir, "../../examples/logfiles/crack_log.lammps"))

if not os.path.exists(candidate_path):
    # Fallback: maybe we are in docs/_build/something
    # Let's try to find the file from the current working directory
    # If we are running from 'docs', then examples is ../examples
    candidate_path = os.path.abspath(os.path.join(os.getcwd(), "../examples/logfiles/crack_log.lammps"))

log_path = candidate_path

# Read the log file
data = lammps_logfile.read_log(log_path)

# Plot Temperature vs Step
plt.figure(figsize=(8, 5))
plt.plot(data['Step'], data['Temp'], label='Temperature')
plt.xlabel('Step')
plt.ylabel('Temperature (K)')
plt.title('Temperature Evolution')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
