# LCMA Form Annotation Standard Specification

This document specifies how annotation labels need to be structure in order to conform to the syntax devised
at the Linz Computational Music Analysis (LCMA) group. The syntax is being encoded in Extended Backus-Naur Form (EBNF)
and [visualised](index.md) using railroad diagrams generated on https://www.bottlecaps.de/rr/ui .
The grammar is contained in the file [lcma_standard.ebnf](lcma_standard.ebnf) in this directory.

## Setup

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Validator

The validator (`validate.py`) checks whether form-label expressions conform to the LCMA grammar.
It can be invoked in several ways, summarized in the table below.

### Options at a glance

| Flag | Long form | Argument | Description |
|------|-----------|----------|-------------|
| `-e` | `--expression` | `STRING` | Validate a single expression passed on the command line |
| `-f` | `--file` | `FILE` | Validate a single expression contained in a text file |
| `-c` | `--csv` | `FILE` | Validate all expressions in a CSV file (must have an `expression` column) |
| `-j` | `--json` | `FILE` | Extract and validate expressions from a structured JSON file |
| `-d` | `--directory` | `DIR` | Recursively scan a directory for JSON files and validate all of them |
| `-o` | `--output` | `PATH` | Control where report CSV files are written |
| `-v` | `--verbose` | — | Show detailed parse trees; print info about skipped files |

### Validating a single expression (`-e`)

Parse and validate one expression directly from the command line. The parsed `AnnotationLabel`
is always printed; pass `-v` to also see the raw parse tree. Use `-o` to additionally write a
single-row report CSV:

```bash
python validate.py -e "ant"
python validate.py -e "theme|pd" -v
python validate.py -e "ant" -o reports/
# writes reports/lcma_validation_report.csv
```

### Validating an expression from a text file (`-f`)

Parse a text file containing a single expression. Like `-e`, always prints the `AnnotationLabel`
and optionally the parse tree with `-v`. Use `-o` to write a report CSV:

```bash
python validate.py -f test_symbol
python validate.py -f test_symbol -o my_report.csv
```

### Validating expressions from a CSV file (`-c`)

The CSV file must contain at least a column named `expression`. The validator iterates over all
rows, parses each expression, and adds/updates the columns `passing` (bool) and `output`
(parse result or error message). The CSV file is **modified in place**.

```bash
python validate.py -c test_cases.csv
```

### Validating expressions from a JSON file (`-j`)

Accepts a JSON file whose first top-level key is `"timelines"`. The validator extracts components
from all timelines of `kind: HIERARCHY_TIMELINE`, collecting each component's `label` as the
expression to validate. The resulting report CSV contains:

1. **Core columns:** `passing`, `expression`, `output`, `description`
2. **Component properties:** all fields from each component object (e.g., `start`, `end`, `level`, `start_measure`, …)
3. **Timeline properties:** the parent timeline's properties, prefixed with `timeline.` (e.g., `timeline.name`, `timeline.ordinal`)
4. **Media metadata:** the file's top-level `media_metadata`, prefixed with `media_metadata.` (e.g., `media_metadata.composer`)

By default, the report is written next to the JSON file with the suffix `.report.csv`:

```bash
python validate.py -j test_files/D790ländler03.json
# creates test_files/D790ländler03.report.csv
```

Use `-o` to redirect the output (see below).

### Validating a directory of JSON files (`-d`)

Recursively scans a directory for `.json` files with the expected format and processes each one.
Files that do not match (no `"timelines"` key or no `HIERARCHY_TIMELINE`) are silently skipped
(use `-v` to see which files are skipped).

The behaviour depends on `-o`:

1. **Without `-o`:** each JSON file gets a sibling `.report.csv`.

   ```bash
   python validate.py -d test_files/
   ```

2. **`-o` with a directory:** reports are placed in that directory with automatic names
   (the directory is created if it does not exist).

   ```bash
   python validate.py -d test_files/ -o test_files/reports
   ```

3. **`-o` with a `.csv` or `.tsv` filepath:** all expressions from all valid JSON files are
   concatenated into a single DataFrame and validated together. The first column, `filename`,
   holds the name of each expression's JSON file, and the last column, `source_file`, its full path.

   ```bash
   python validate.py -d test_files/ -o all_expressions.csv
   ```

### Controlling report output (`-o`)

The `-o` flag works with all input modes:

- **With `-e`:** writes a single-row report CSV. Without `-o`, only terminal output is shown.
  If `-o` points to a directory, the default filename `lcma_validation_report.csv` is used.
- **With `-f`:** same as `-e`, but the default filename is derived from the input file
  (e.g., `test_symbol.report.csv`).
- **With `-j`/`-d`:** if the path ends in `.csv` or `.tsv`, it is used as a file path directly.
  Otherwise, it is treated as a directory (created if needed), and report files are placed inside
  with automatic names (`<stem>.report.csv`).

```bash
python validate.py -e "ant" -o my_report.csv
python validate.py -j test_files/D790ländler03.json -o reports/
```

### Verbose output (`-v`)

Pass `-v` to show detailed parse trees (the raw dict from the parser) in addition to the
`AnnotationLabel` output. For batch modes (`-c`, `-j`, `-d`), this also prints parse trees for
each expression and reports skipped files:

```bash
python validate.py -e "ant" -v
python validate.py -d test_files/ -v
```

## For developers

### TL;DR: updating the annotation standard

1. **Grammar:** edit [lcma_standard.ebnf](lcma_standard.ebnf), e.g. add the new label (with its
   abbreviation) to `SpecificFunction`, `Unit` or `FormalType`. Do not use `/regex/` literals
   (see [Generating railroad diagrams](#generating-railroad-diagrams)).
2. **Python code:** mirror the change in `src/musicalform/enums.py` by adding the member and its
   alias to the matching enum (`SpecificFunctionName`, `UnitName`, `MainType`, …):

   ```python
   middle = auto()
   mid = middle
   ```

   New syntax (operators, label structure) additionally needs handling in
   `src/musicalform/core.py` and tests in `tests/test_core.py`.
3. **Parser and diagrams:** regenerate both, then review the diff of
   `src/musicalform/cli/lcma_standardParser.py`:

   ```bash
   python grammar/update_parser.py --rr path/to/rr.war
   ```

4. **Tests:** `pytest` (or `tox` for all Python versions).
5. **Validation:** re-validate the annotation corpus from your local clone of `annotation_pilot`
   and check how the report changed:

   ```bash
   musicalform validate -d ~/annotation_pilot/TiLiA -o grammar/validation_report.csv
   ```

6. **Commit** everything together with a [conventional commit](https://www.conventionalcommits.org/)
   message and push to `development` (or open a PR against it):
   - `feat(grammar): adds the term contrasting middle` for new labels or syntax
   - `fix(grammar): …` for corrections
   - `chore(validation): updates validation_report.csv for annotation_pilot@<commit>` for
     report-only updates

   Release Please only picks up `feat` and `fix` commits (and breaking changes) for releases;
   see [Workflow](../README.md#workflow).
7. **Release:** Release Please opens (or updates) a release PR on `development` that bumps the
   version in `pyproject.toml` and updates `CHANGELOG.md`. Merging it creates the tag and the
   GitHub release. To also publish to PyPI, run `tox -e build` and `tox -e publish`
   (see [Release Process](../README.md#release-process)).
8. **Guidelines repository:** commit the new submodule pointer in the parent repository with
   `git add musicalform` and `git commit`.

### Pre-commit hooks

Before making changes to the validator or other Python code, install the pre-commit hooks:

```bash
pre-commit install
```

This enables automatic formatting (black, isort) and linting (flake8) checks on every commit.

### Regenerating the parser

The parser (`lcma_standardParser.py`) is auto-generated from the EBNF grammar by
[DHParser](https://gitlab.lrz.de/badw-it/DHParser). After modifying `lcma_standard.ebnf`,
regenerate the parser and install it into the package with:

```bash
python grammar/update_parser.py
```

This does the same as `dhparser lcma_standard.ebnf` and then moves the generated parser to
`src/musicalform/cli/lcma_standardParser.py`, the copy that `musicalform validate` actually uses.
Only the `PARSER SECTION` is regenerated; the editable sections (preprocessor, AST
transformations, compiler) are preserved. Always review the diff before committing.

### Debugging with the generated parser

The generated parser can be run directly on text files to inspect parse trees and produce
detailed log files for debugging. It requires a text file containing a single expression
(it does not accept expressions on the command line). Pass `-d` to enable debug mode, which
writes log files to the `LOGS/` subdirectory:

```bash
python lcma_standardParser.py -d test_symbol
```

This produces several files in `LOGS/`, of which `LOGS/test_symbol_parser.log.html` is the most
useful: it shows the step-by-step parsing trace as an interactive HTML document, making it easy
to pinpoint where and why a parse fails.

Additional flags:

| Flag | Description |
|------|-------------|
| `-d` | Enable debug mode (write logs to `LOGS/`) |
| `-v` | Verbose output |
| `-f` | Write output even if errors occurred |
| `-o DIR` | Output directory for batch processing |
| `-s FMT` | Serialization format(s) for the output |

You can also batch-process multiple files or an entire directory:

```bash
python lcma_standardParser.py -d -o out/ file1.txt file2.txt
python lcma_standardParser.py -d -o out/ test_files_dir/
```

### Generating railroad diagrams

The railroad diagrams in [index.md](index.md) and `diagram/` are generated by
[RR](https://github.com/GuntherRademacher/rr). `update_parser.py` can regenerate them along with
the parser if you pass the path to `rr.war`:

```bash
python grammar/update_parser.py --rr path/to/rr.war
```

`rr.war` is available from Maven Central, e.g.
[rr-webapp-2.6.war](https://repo1.maven.org/maven2/de/bottlecaps/rr/rr-webapp/2.6/rr-webapp-2.6.war),
and requires Java 11 or newer. If the `java` on your `PATH` is older, pass a newer one with
`--java path/to/java`.

RR only understands W3C-style EBNF, so the script drops DHParser's `~` markers (outside of
string literals and character classes) from a temporary copy of the grammar. For the same
reason, `lcma_standard.ebnf` must not use DHParser's `/regex/` literals; use character classes
and alternatives instead. Keep in mind that DHParser is a PEG parser, which does not backtrack
into optional elements: `[2-9]? '2nd'` would not match `2nd`.
