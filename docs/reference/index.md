# API Reference

## Log Reader

```{eval-rst}
.. autofunction:: lammps_logfile.read_log
```

## Utilities

```{eval-rst}
.. automodule:: lammps_logfile.utils
    :members:
```

## Command Line Interface

`lammps-logfile` includes a command-line interface (CLI) tool called `lammps_logplotter` for quick visualization of log files without writing any Python code.

```{argparse}
:module: lammps_logfile.cmd_interface
:func: get_parser
:prog: lammps_logplotter
```
