# Contributing

## Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/henriasv/lammps-logfile.git
    cd lammps-logfile
    ```

2.  Install in editable mode with dependencies:
    ```bash
    pip install -e .[docs]
    ```

## Testing

Run tests using `pytest` (or `unittest` if preferred):

```bash
pytest
```

## Building Documentation

To build the documentation locally:

```bash
cd docs
make html
```

The HTML files will be in `docs/_build/html`.
