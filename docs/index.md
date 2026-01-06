# lammps-logfile

```{image} https://img.shields.io/pypi/v/lammps-logfile.svg
:target: https://pypi.org/project/lammps-logfile/
:alt: PyPI Version
```
```{image} https://img.shields.io/pypi/pyversions/lammps-logfile.svg
:target: https://pypi.org/project/lammps-logfile/
:alt: Python Versions
```
```{image} https://github.com/henriasv/lammps-logfile/workflows/Install%20and%20tests/badge.svg
:target: https://github.com/henriasv/lammps-logfile/actions
:alt: Build Status
```

**From LAMMPS log files to Analysis-Ready Data in one line of code.**

`lammps-logfile` is a high-performance Python library designed to simplify the extraction and analysis of thermodynamic data from [LAMMPS](https://lammps.sandia.gov) simulations. Stop writing fragile regex parsers and start analyzing your physics.

## Key Features

::::{grid} 1 1 2 3

:::{grid-item}
:class: sd-card

**High Performance**
Fast parsing of multi-gigabyte log files using optimized routines.
:::

:::{grid-item}
:class: sd-card

**Pandas Integration**
Direct conversion to Pandas DataFrames for instant plotting and analysis.
:::

:::{grid-item}
:class: sd-card

**Robustness**
Handles multiple runs, `thermo_style` changes, and partial logs seamlessly.
:::

::::

## Code at a Glance

```python
import lammps_logfile
import matplotlib.pyplot as plt

# Load data with a single line
data = lammps_logfile.read_log("log.lammps")

# Access thermodynamic properties directly as a DataFrame
plt.plot(data["Step"], data["Temp"])
plt.xlabel("Step")
plt.ylabel("Temperature (K)")
plt.show()
```

## Documentation

```{toctree}
:maxdepth: 2
:hidden:

getting_started/index
user_guide/index
api_reference/index
examples/index
development/index
citing
```
