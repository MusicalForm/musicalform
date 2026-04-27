"""musicalform convert — convert TiLiA JSON exports into per-timeline CSVs.

Each JSON file produces one CSV per timeline, named so that TiLiA can
re-import them. With multiple timelines of the same kind, files are numbered.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from musicalform.tilia import (
    export_timelines_to_csv,
    parse_tilia_json,
)


def _resolve_out_folder(
    json_path: Path,
    output: Optional[str | Path],
) -> Path:
    """Resolve the directory in which to write CSVs for a given JSON file.

    No `-o`: write next to the JSON file. `-o DIR`: write into DIR (created if needed).
    """
    if output is None:
        return json_path.parent
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    return out


def process_json_file(
    json_path: str | Path,
    output: Optional[str | Path] = None,
    all_columns: bool = False,
    verbose: bool = False,
) -> list[Path]:
    """Convert a single TiLiA JSON file into per-timeline CSVs."""
    json_path = Path(json_path)
    kind2dfs = parse_tilia_json(json_path, only_import_columns=not all_columns)
    if not kind2dfs:
        if verbose:
            print(f"Skipping {json_path}: not a valid TiLiA JSON or no timelines with components.")
        return []

    out_folder = _resolve_out_folder(json_path, output)
    return export_timelines_to_csv(kind2dfs, json_path.stem, out_folder=out_folder)


def process_json_directory(
    directory: str | Path,
    output: Optional[str | Path] = None,
    all_columns: bool = False,
    verbose: bool = False,
) -> list[Path]:
    """Recursively convert every TiLiA JSON file under `directory`.

    No `-o`: each JSON gets its CSVs as siblings.
    `-o DIR`: every JSON's CSVs are written into DIR.
    """
    directory = Path(directory)
    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    json_files = sorted(directory.rglob("*.json"))
    if not json_files:
        print(f"No JSON files found in {directory}")
        return []

    written: list[Path] = []
    for json_file in json_files:
        try:
            paths = process_json_file(json_file, output=output, all_columns=all_columns, verbose=verbose)
        except Exception as e:
            print(f"Failed to convert {json_file}: {e}")
            continue
        written.extend(paths)

    if not written:
        print(f"No valid TiLiA JSON files found in {directory}")
    return written


def main(
    json_file: Optional[str] = None,
    json_dir: Optional[str] = None,
    output: Optional[str] = None,
    all_columns: bool = False,
    verbose: bool = False,
) -> None:
    if json_file is None and json_dir is None:
        raise ValueError("At least one of -j/--json or -d/--directory must be provided.")
    if json_file:
        process_json_file(json_file, output=output, all_columns=all_columns, verbose=verbose)
    if json_dir:
        process_json_directory(json_dir, output=output, all_columns=all_columns, verbose=verbose)
