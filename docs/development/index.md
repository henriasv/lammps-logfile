# Development

We welcome contributions!

```{toctree}
:maxdepth: 2

contributing
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
