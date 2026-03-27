"""Top-level entry point for the `musicalform` command-line interface.

Dispatches subcommands:
    musicalform validate [...]   — validate LCMA form-annotation labels
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="musicalform",
        description="musicalform: tools for LCMA musical form annotation.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", metavar="SUBCOMMAND")
    subparsers.required = True

    # ---- validate subcommand ------------------------------------------------
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate LCMA form-annotation labels against the current grammar.",
        description="Test expressions, files, CSVs, or JSON timeline files against the current grammar.",
    )
    validate_parser.add_argument("-e", "--expression", help="A string expressing a form label.")
    validate_parser.add_argument("-f", "--file", help="A text file containing a form label.")
    validate_parser.add_argument(
        "-c",
        "--csv",
        help="A CSV file with an 'expression' column. The 'passing' and 'output' columns are "
        "added/updated in-place.",
    )
    validate_parser.add_argument(
        "-j",
        "--json",
        help="A JSON file with 'timelines' as its first top-level key. Components from "
        "HIERARCHY_TIMELINEs are extracted, validated, and saved as a report CSV.",
    )
    validate_parser.add_argument(
        "-d",
        "--directory",
        help="A directory to recursively scan for JSON files with HIERARCHY_TIMELINEs.",
    )
    validate_parser.add_argument(
        "-o",
        "--output",
        help="Output path for report files. A .csv/.tsv path is used as-is; a directory "
        "receives auto-named reports. Default for -j/-d: sibling .report.csv files.",
    )
    validate_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show parse trees and information about skipped files.",
    )

    return parser


def run():
    parser = build_parser()
    args = parser.parse_args()

    if args.subcommand == "validate":
        from musicalform.cli.validate import main as validate_main

        validate_main(
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
