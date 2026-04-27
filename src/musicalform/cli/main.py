"""Top-level entry point for the `musicalform` command-line interface.

Dispatches subcommands:
    musicalform validate [...]   — validate LCMA form-annotation labels
    musicalform convert  [...]   — convert TiLiA JSON exports to per-timeline CSVs
"""

from __future__ import annotations

import argparse

from musicalform import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="musicalform",
        description="musicalform: tools for LCMA musical form annotation.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
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

    # ---- convert subcommand -------------------------------------------------
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert TiLiA JSON exports into per-timeline CSVs ready for re-import.",
        description="Each JSON file is split into one CSV per timeline; multiple timelines "
        "of the same kind are numbered. Default columns match what TiLiA imports.",
    )
    convert_parser.add_argument(
        "-j",
        "--json",
        help="A TiLiA JSON file with 'timelines' as its first top-level key.",
    )
    convert_parser.add_argument(
        "-d",
        "--directory",
        help="A directory to recursively scan for TiLiA JSON files.",
    )
    convert_parser.add_argument(
        "-o",
        "--output",
        help="Output folder for the generated CSVs. Default: next to each JSON file.",
    )
    convert_parser.add_argument(
        "-a",
        "--all-columns",
        action="store_true",
        help="Keep all non-empty columns instead of filtering to the TiLiA-import set.",
    )
    convert_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print information about skipped files.",
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
    elif args.subcommand == "convert":
        from musicalform.cli.convert import main as convert_main

        convert_main(
            json_file=args.json,
            json_dir=args.directory,
            output=args.output,
            all_columns=args.all_columns,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    run()
