"""Parsing TiLiA JSON exports into per-timeline DataFrames and writing them
back out as TiLiA-importable CSV files.

The shapes produced here mirror what `processing.tta.parsing.parse_tilia_json`
(deprecated) produces, but built directly from the JSON without that
dependency. Each row in a per-timeline DataFrame is a component; the parent
timeline's `name` is injected as a column on every row, which TiLiA's CSV
import expects.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Iterator, Optional

import pandas as pd

TYPE2COLUMNS: dict[str, list[str]] = {
    "beat": [
        "name",
        "time",
        "is_first_in_measure",
        "measure",
        "beat",
    ],
    "harmony": [
        "name",
        "time",
        "measure",
        "beat",
        "harmony_or_key",
        "level",
        "step",
        "accidental",
        "quality",
        "type",
        "inversion",
        "applied_to",
        "display_mode",
        "custom_text",
        "custom_text_font_type",
        "comments",
    ],
    "hierarchy": [
        "name",
        "start",
        "end",
        "start_measure",
        "end_measure",
        "level",
        "pre_start",
        "post_end",
        "label",
        "comments",
        "formal_function",
        "formal_type",
    ],
    "marker": [
        "name",
        "time",
        "measure",
        "label",
        "comments",
    ],
    "pdf": [
        "name",
        "time",
        "measure",
        "page_number",
    ],
}


TILIA_COLUMN_DTYPES: dict[str, str | type] = {
    "time": float,
    "level": "Int64",
    "measure": "Int64",
    "beat": "Int64",
    "start_beat": "Int64",
    "end_beat": "Int64",
    "start_measure": "Int64",
    "end_measure": "Int64",
    "page_number": "Int64",
    "label": "string",
    "comments": "string",
}


def update_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    dtypes = {col: dtype for col, dtype in TILIA_COLUMN_DTYPES.items() if col in df.columns}
    return df.astype(dtypes) if dtypes else df


def is_valid_tilia_json(data: object) -> bool:
    """A TiLiA JSON has 'timelines' as its first top-level key."""
    if not isinstance(data, dict):
        return False
    return next(iter(data), None) == "timelines"


def kind_to_short(kind: str) -> str:
    """`'BEAT_TIMELINE'` -> `'beat'`."""
    return kind.lower().split("_")[0]


def iter_timeline_components(
    json_path: str | Path,
    *,
    kinds: Optional[Iterable[str]] = None,
) -> Iterator[tuple[dict, dict, pd.DataFrame]]:
    """Yield `(timeline_props, media_metadata, components_df)` for every timeline
    in `json_path` whose `kind` is in `kinds` (all kinds if `kinds is None`).

    `components_df` is `pd.json_normalize`'d component records; `timeline_props`
    is the timeline dict without its `components` field. Timelines with no
    components are skipped.
    """
    json_path = Path(json_path)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not is_valid_tilia_json(data):
        return

    media_metadata = data.get("media_metadata", {}) or {}
    kind_filter = set(kinds) if kinds is not None else None

    for tl in data.get("timelines", []) or []:
        kind = tl.get("kind")
        if kind_filter is not None and kind not in kind_filter:
            continue
        components = tl.get("components", []) or []
        if not components:
            continue
        df = pd.json_normalize(components)
        tl_props = {k: v for k, v in tl.items() if k != "components"}
        yield tl_props, media_metadata, df


def _prepare_import_df(
    df: pd.DataFrame,
    tl_props: dict,
    kind_short: str,
    *,
    only_import_columns: bool,
) -> pd.DataFrame:
    """Bring a per-timeline component DataFrame into TiLiA-import shape.

    Injects the timeline's `name`, renames the component-level `kind` to
    `component`, derives `is_first_in_measure` for beat timelines, applies dtypes,
    and (optionally) filters to `TYPE2COLUMNS[kind_short]`.
    """
    if "kind" in df.columns:
        if kind_short == "harmony":
            df = df.rename(columns={"kind": "harmony_or_key"})
            df["harmony_or_key"] = df["harmony_or_key"].str.lower().replace({"mode": "key"})
        else:
            df = df.rename(columns={"kind": "component"})
    df["name"] = tl_props.get("name")

    if kind_short == "beat" and "beat" in df.columns:
        is_first = (df["beat"] == 1).map({True: "true", False: "false"}).rename("is_first_in_measure")
        df = pd.concat([df, is_first], axis=1)
        if "measure" in df.columns:
            df = df.dropna(subset="measure")

    df = update_dtypes(df)

    if only_import_columns:
        if kind_short in TYPE2COLUMNS:
            columns = TYPE2COLUMNS[kind_short]
            for col in columns:
                if col not in df.columns:
                    df[col] = pd.NA
            df = df[columns]
        else:
            df = df.dropna(axis=1, how="all")
    else:
        df = df.dropna(axis=1, how="all")

    return df


def parse_tilia_json(
    json_path: str | Path,
    *,
    kinds: Optional[Iterable[str]] = None,
    only_import_columns: bool = True,
) -> dict[str, list[pd.DataFrame]]:
    """Parse a TiLiA JSON export into per-kind, per-timeline DataFrames.

    Returns a `{kind_short: [df, df, ...]}` mapping where `kind_short` is e.g.
    `'beat'` for `'BEAT_TIMELINE'` and the list contains one DataFrame per
    timeline of that kind, in TiLiA-import-ready shape. Timelines without
    components are skipped; if `kinds` is given, only those JSON kind strings
    (e.g. `'HIERARCHY_TIMELINE'`) are returned.
    """
    result: dict[str, list[pd.DataFrame]] = defaultdict(list)
    for tl_props, _, df in iter_timeline_components(json_path, kinds=kinds):
        kind_short = kind_to_short(tl_props.get("kind", ""))
        prepared = _prepare_import_df(df, tl_props, kind_short, only_import_columns=only_import_columns)
        result[kind_short].append(prepared)
    return dict(result)


def _store_csv(df: pd.DataFrame, stem: str, suffix: str, out_folder: Optional[str | Path]) -> Path:
    csv_name = f"{stem}.{suffix}.csv"
    csv_path = Path(out_folder) / csv_name if out_folder else Path(csv_name)
    df.to_csv(csv_path, index=False)
    print(f"Wrote {csv_path}")
    return csv_path


def export_timelines_to_csv(
    kind2dfs: dict[str, list[pd.DataFrame]],
    stem: str,
    out_folder: Optional[str | Path] = None,
) -> list[Path]:
    """Write one CSV per timeline.

    Single timeline of a kind -> `{stem}.{kind}.csv`.
    Multiple timelines of the same kind -> `{stem}.{kind}1.csv`, `{stem}.{kind}2.csv`, ...
    Returns the list of written paths.
    """
    written: list[Path] = []
    for kind_short, dfs in kind2dfs.items():
        if len(dfs) == 1:
            written.append(_store_csv(dfs[0], stem, kind_short, out_folder))
            name = dfs[0]["name"].iloc[0] if "name" in dfs[0].columns and len(dfs[0]) else None
            if name is not None:
                print(name)
        else:
            for i, df in enumerate(dfs, 1):
                suffix = f"{kind_short}{i}"
                written.append(_store_csv(df, stem, suffix, out_folder))
                name = df["name"].iloc[0] if "name" in df.columns and len(df) else None
                if name is not None:
                    print(f"{suffix}: {name}")
    return written
