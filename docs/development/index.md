# Development

We welcome contributions!

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

## Running Tests

We use `pytest` for testing. To run the test suite:

```bash
pip install -e .[test]
pytest
```

## Building Documentation

To build the documentation locally:

1. Install documentation dependencies:
   ```bash
   pip install -r docs/requirements.txt
   ```
2. Build HTML:
   ```bash
   cd docs
   make html
   ```
3. Open `docs/_build/html/index.html` in your browser.
