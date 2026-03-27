# musicalform

A Python library and infrastructure for modelling musical form.

[![PyPI version](https://img.shields.io/pypi/v/musicalform.svg)](https://pypi.org/project/musicalform/)
[![Python versions](https://img.shields.io/pypi/pyversions/musicalform.svg)](https://pypi.org/project/musicalform/)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](https://unlicense.org/)

---

## Installation

```bash
pip install musicalform
```

**Requirements:** Python 3.11+, DHParser 1.8.3+

---

## CLI

The package ships a `validate` command that tests LCMA form-annotation labels against the current grammar:

```bash
# Validate a single expression
musicalform validate -e "bi"

# Validate a text file
musicalform validate -f my_label.txt

# Validate all expressions in a CSV (column: 'expression')
musicalform validate -c annotations.csv

# Extract and validate from a JSON timeline file
musicalform validate -j piece.json -o reports/

# Recursively process a directory of JSON files
musicalform validate -d data/ -o all_results.csv

# Verbose mode (show parse trees and skipped files)
musicalform validate -e "bi" -v
```

---

## Development

```bash
git clone <repo-url>
cd musicalform

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
tox -e py311
# or
pytest

# Run linters
tox -e lint

# Auto-format code
tox -e format

# Build package
tox -e build
```

---

## License

This project is released into the public domain under the [Unlicense](https://unlicense.org/).
See [LICENSE](LICENSE) for details.
