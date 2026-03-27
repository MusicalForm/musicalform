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

### Getting Started

```bash
git clone <repo-url>
cd musicalform

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests and Checks

```bash
# Run tests for all supported Python versions
tox

# Run tests for a specific Python version
tox -e py311
tox -e py312

# Or use pytest directly
pytest

# Run linters
tox -e lint

# Run type checking
tox -e typecheck
```

### Workflow

All pull requests should target the **`development`** branch. Commits follow [conventional commit](https://www.conventionalcommits.org/) format, which enables semantic versioning:

| Commit Message | Version Bump | Emoji |
|---|---|---|
| `feat: add new feature` | Minor (0.x.0) | ✨ |
| `fix: resolve issue` | Patch (0.0.x) | 🐛 |
| `BREAKING CHANGE: description` | Major (x.0.0) | ⚠️ |
| `docs: update documentation` | No release | 📚 |
| `refactor: reorganize code` | No release | ♻️ |
| `test: add tests` | No release | ✅ |
| `perf: improve performance` | No release | ⚡ |
| `chore: maintenance tasks` | No release | 🔧 |

### Release Process

When commits are pushed to `development`, [Release Please](https://github.com/googleapis/release-please) automatically:

1. Analyzes conventional commit messages
2. Creates a PR with bumped version in `pyproject.toml` and updated `CHANGELOG.md`
3. When merged, creates a GitHub Release

To publish to PyPI after a release is created:

```bash
# Build the package
tox -e build

# Publish to PyPI (requires TWINE_API_TOKEN in environment)
tox -e publish
```

Check your version at any time with:

```bash
musicalform --version
```

---

## License

This project is released into the public domain under the [Unlicense](https://unlicense.org/).
See [LICENSE](LICENSE) for details.
