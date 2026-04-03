"""musicalform validate — CLI for validating LCMA form-annotation labels.

This module is the entry point for the `musicalform validate` command.
It imports all domain objects from the musicalform library and provides
the full validation logic: expression, file, CSV, and JSON/directory modes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from pprint import pprint
from typing import Optional, Tuple

import pandas as pd
from DHParser import RootNode

# NOTE: lcma_standardParser.py lives alongside this file in the cli/ package.
from musicalform.cli.lcma_standardParser import compile_src

# All domain objects come from the musicalform library.
from musicalform.core import AnnotationLabel
from musicalform.utils import parse_expression_as_dict

VERBOSE = False


# ---------------------------------------------------------------------------
# Parse tree -> AnnotationLabel
# ---------------------------------------------------------------------------


def parse_tree(tree: dict) -> AnnotationLabel:
    if VERBOSE:
        pprint(tree, sort_dicts=False)
    return AnnotationLabel.from_parse(tree)


# ---------------------------------------------------------------------------
# Raw parse functions (DHParser -> dict -> objects)
# ---------------------------------------------------------------------------


def parse_file(file):
    T: Tuple[RootNode, list] = compile_src(file)
    result, errors = T
    return result


def parse_file_as(file, format):
    result = parse_file(file)
    return result.serialize(format)


def parse_file_as_dict(file) -> dict:
    json_str = parse_file_as(file, "jsondict")
    tree = json.loads(json_str)
    return tree


def parse_file_as_objects(file="test_symbol") -> AnnotationLabel:
    tree_dict = parse_file_as_dict(file)
    return parse_tree(tree_dict)


def parse_expression_as_objects(exp: str) -> AnnotationLabel:
    tree_dict = parse_expression_as_dict(exp)
    return parse_tree(tree_dict)


# ---------------------------------------------------------------------------
# CSV processing
# ---------------------------------------------------------------------------


def parse_csv_file(csv_file: str):
    # Load the CSV file
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        raise ValueError(f"Error loading CSV file: {e}")

    if "expression" not in df.columns:
        raise ValueError("CSV file must contain an 'expression' column")

    if "passing" not in df.columns:
        df["passing"] = pd.Series([False] * len(df), dtype=bool)
    else:
        df["passing"] = df["passing"].astype(bool)
    if "output" not in df.columns:
        df["output"] = ""
    else:
        df["output"] = df["output"].astype(str)

    for idx, row in df.iterrows():
        expression = row["expression"]
        try:
            parsed_result = parse_expression_as_objects(expression)
            df.at[idx, "passing"] = True
            df.at[idx, "output"] = str(parsed_result)
        except Exception as e:
            df.at[idx, "passing"] = False
            df.at[idx, "output"] = str(e)

    df.to_csv(csv_file, index=False)
    passing = df.passing.sum()
    failing = len(df) - passing
    print(f"Processed {len(df)} expressions: {passing} passed, {failing} failed. Results saved to {csv_file}")


# ---------------------------------------------------------------------------
# JSON processing
# ---------------------------------------------------------------------------


def is_valid_json_format(data: dict) -> bool:
    """Check if a JSON dict has 'timelines' as its first top-level key."""
    if not isinstance(data, dict):
        return False
    first_key = next(iter(data), None)
    return first_key == "timelines"


def json_to_dataframe(json_path: str | Path) -> Optional[pd.DataFrame]:
    """Extract HIERARCHY_TIMELINE components from a JSON file into a DataFrame.

    Returns a DataFrame with columns: passing, expression, output, description,
    <component properties>, <timeline properties>, <media_metadata properties>.
    Returns None if the file doesn't have the expected format or no HIERARCHY_TIMELINEs.
    """
    json_path = Path(json_path)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not is_valid_json_format(data):
        return None

    media_metadata = data.get("media_metadata", {})
    hierarchy_timelines = [tl for tl in data.get("timelines", []) if tl.get("kind") == "HIERARCHY_TIMELINE"]

    if not hierarchy_timelines:
        return None

    all_frames = []
    for tl in hierarchy_timelines:
        components = tl.get("components", [])
        if not components:
            continue

        df_components = pd.json_normalize(components)

        tl_props = {k: v for k, v in tl.items() if k != "components"}
        for key, val in tl_props.items():
            df_components[f"timeline.{key}"] = val

        for key, val in media_metadata.items():
            df_components[f"media_metadata.{key}"] = val

        all_frames.append(df_components)

    if not all_frames:
        return None

    df = pd.concat(all_frames, ignore_index=True)

    if "label" in df.columns:
        df = df.rename(columns={"label": "expression"})

    for col, default in [
        ("passing", False),
        ("expression", ""),
        ("output", ""),
        ("description", ""),
    ]:
        if col not in df.columns:
            df[col] = default

    core_cols = ["passing", "expression", "output", "description"]
    comp_cols = [
        c
        for c in df.columns
        if not c.startswith("timeline.") and not c.startswith("media_metadata.") and c not in core_cols
    ]
    timeline_cols = sorted(c for c in df.columns if c.startswith("timeline."))
    metadata_cols = sorted(c for c in df.columns if c.startswith("media_metadata."))

    ordered_cols = core_cols + comp_cols + timeline_cols + metadata_cols
    df = df[ordered_cols]

    return df


def resolve_output_path(
    json_path: str | Path,
    output: Optional[str | Path] = None,
) -> Path:
    """Determine the output CSV path for a given JSON file.

    Args:
        json_path: Path to the source JSON file.
        output: Optional -o argument. Can be:
            - None: report file is placed next to the JSON file with .report.csv suffix.
            - A path ending in .csv or .tsv: used as-is (for single-file output).
            - A directory path: report file placed in that directory with automatic naming.

    Returns:
        The resolved output Path.
    """
    json_path = Path(json_path)
    default_name = json_path.stem + ".report.csv"

    if output is None:
        return json_path.parent / default_name

    output = Path(output)
    if output.suffix.lower() in (".csv", ".tsv"):
        return output

    output.mkdir(parents=True, exist_ok=True)
    return output / default_name


def process_json_file(
    json_path: str | Path,
    output: Optional[str | Path] = None,
    verbose: bool = False,
) -> Optional[Path]:
    """Process a single JSON file: extract to CSV, then validate.

    Returns the path to the generated report CSV, or None if the file was skipped.
    """
    json_path = Path(json_path)
    df = json_to_dataframe(json_path)
    if df is None:
        if verbose:
            print(f"Skipping {json_path}: not a valid format or no HIERARCHY_TIMELINEs found.")
        return None

    csv_path = resolve_output_path(json_path, output)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"Extracted {len(df)} components from {json_path} -> {csv_path}")

    parse_csv_file(str(csv_path))
    return csv_path


def process_json_directory(
    directory: str | Path,
    output: Optional[str | Path] = None,
    verbose: bool = False,
) -> list[Path]:
    """Recursively process all JSON files in a directory.

    Behaviour depends on -o:
        1. No -o: each JSON file gets a sibling .report.csv
        2. -o is a directory: reports are created in that directory with automatic names
        3. -o is a .csv/.tsv file: all expressions are concatenated into one file before validation

    Returns a list of generated report CSV paths.
    """
    directory = Path(directory)
    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    concat_mode = False
    if output is not None:
        output_path = Path(output)
        if output_path.suffix.lower() in (".csv", ".tsv"):
            concat_mode = True

    json_files = sorted(directory.rglob("*.json"))

    if not json_files:
        print(f"No JSON files found in {directory}")
        return []

    if concat_mode:
        all_frames = []
        for json_file in json_files:
            df = json_to_dataframe(json_file)
            if df is None:
                if verbose:
                    print(f"Skipping {json_file}: not a valid format or no HIERARCHY_TIMELINEs found.")
                continue
            df.insert(0, "source_file", str(json_file))
            all_frames.append(df)

        if not all_frames:
            print(f"No valid JSON files with HIERARCHY_TIMELINEs found in {directory}")
            return []

        combined_df = pd.concat(all_frames, ignore_index=True)
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        combined_df.to_csv(output_path, index=False)
        print(f"Extracted {len(combined_df)} total components from {len(all_frames)} files -> {output_path}")

        parse_csv_file(str(output_path))
        return [output_path]

    report_paths = []
    for json_file in json_files:
        result = process_json_file(json_file, output=output, verbose=verbose)
        if result is not None:
            report_paths.append(result)

    if not report_paths:
        print(f"No valid JSON files with HIERARCHY_TIMELINEs found in {directory}")

    return report_paths


# ---------------------------------------------------------------------------
# Argument dispatch
# ---------------------------------------------------------------------------

DEFAULT_REPORT_NAME = "lcma_validation_report.csv"


def _resolve_single_output(
    output: Optional[str | Path],
    default_stem: Optional[str] = None,
) -> Optional[Path]:
    """Resolve -o for single-expression modes (-e, -f).

    Returns None if no output was requested, otherwise the resolved Path.
    """
    if output is None:
        return None
    output = Path(output)
    if output.suffix.lower() in (".csv", ".tsv"):
        return output
    output.mkdir(parents=True, exist_ok=True)
    name = (default_stem + ".report.csv") if default_stem else DEFAULT_REPORT_NAME
    return output / name


def _validate_and_report(
    expression: str,
    output_path: Path,
) -> None:
    """Validate a single expression and write/update a one-row report CSV."""
    try:
        parsed_result = parse_expression_as_objects(expression)
        passing = True
        result_str = str(parsed_result)
    except Exception as e:
        passing = False
        result_str = str(e)

    df = pd.DataFrame([{"passing": passing, "expression": expression, "output": result_str}])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    status = "passed" if passing else "FAILED"
    print(f"Expression {status}. Report saved to {output_path}")


def main(
    expression: Optional[str] = None,
    txt_file: Optional[str] = None,
    csv_file: Optional[str] = None,
    json_file: Optional[str] = None,
    json_dir: Optional[str] = None,
    output: Optional[str] = None,
    verbose: bool = False,
):
    global VERBOSE
    VERBOSE = verbose
    if all(arg is None for arg in (expression, txt_file, csv_file, json_file, json_dir)):
        raise ValueError("At least one argument must be provided.")

    if expression:
        parsed_expression = parse_expression_as_objects(expression)
        pprint(parsed_expression, sort_dicts=False)
        out_path = _resolve_single_output(output)
        if out_path:
            _validate_and_report(expression, out_path)
    if txt_file:
        parsed_file = parse_file_as_objects(txt_file)
        pprint(parsed_file, sort_dicts=False)
        out_path = _resolve_single_output(output, default_stem=Path(txt_file).stem)
        if out_path:
            with open(txt_file, "r", encoding="utf-8") as f:
                file_expression = f.read().strip()
            _validate_and_report(file_expression, out_path)
    if csv_file:
        parse_csv_file(csv_file)
    if json_file:
        process_json_file(json_file, output=output, verbose=verbose)
    if json_dir:
        process_json_directory(json_dir, output=output, verbose=verbose)


def parse_args():
    parser = argparse.ArgumentParser(description="Test an expression against the current grammar.")
    parser.add_argument("-e", "--expression", help="A string expressing a form label.")
    parser.add_argument("-f", "--file", help="A text file containing a form label.")
    parser.add_argument(
        "-c",
        "--csv",
        help="A CSV file containing at least the column 'expression'. The script will iterate over the expressions "
        "and (add and) update the columns 'passing' and 'output'. The CSV file will be modified and overwritten!",
    )
    parser.add_argument(
        "-j",
        "--json",
        help="A JSON file with 'timelines' as its first top-level key. Components from HIERARCHY_TIMELINEs "
        "are extracted, validated, and saved as a report CSV.",
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="A directory to recursively scan for JSON files with HIERARCHY_TIMELINEs. "
        "Each valid file is processed like -j.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output path for report files. If a .csv/.tsv filepath, used as the output file. "
        "If a directory, reports are placed there with automatic names. "
        "Default for -j/-d: report CSV next to each JSON file. "
        "For -e/-f: no CSV output unless -o is specified.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed parse trees during validation. Also print information "
        "about skipped files when using -d.",
    )
    args = parser.parse_args()
    return args


def run():
    args = parse_args()
    main(
        expression=args.expression,
        txt_file=args.file,
        csv_file=args.csv,
        json_file=args.json,
        json_dir=args.directory,
        output=args.output,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    run()
