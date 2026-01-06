# API Reference

## Log Reader

```{eval-rst}
.. autofunction:: lammps_logfile.read_log
```

## Legacy Interface

The following classes are maintained for backward compatibility. New users should prefer `read_log`.

```{toctree}
:maxdepth: 2

legacy/index
```

## Utilities

```{eval-rst}
.. automodule:: lammps_logfile.utils
    :members:
```

## Command Line Interface

```{eval-rst}
.. argparse::
    :ref: lammps_logfile.cmd_interface.get_parser
    :prog: lammps_logplotter
```
