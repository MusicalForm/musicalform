#!/usr/bin/env python3
"""Regenerate the LCMA parser from lcma_standard.ebnf and install it into the musicalform package.

Equivalent to running ``dhparser lcma_standard.ebnf`` in this directory (it calls the same
``DHParser.dsl.compile_on_disk`` function as the ``dhparser`` command) and then moving the
generated lcma_standardParser.py to src/musicalform/cli/, overwriting the existing one.

DHParser preserves the editable sections (preprocessor, AST transformations, compiler) of an
existing lcma_standardParser.py next to the grammar. Since this script moves that file away,
the package's copy is placed here first if none exists, so that those sections survive.

Optionally (``--rr``), the railroad diagrams in index.md and diagram/ are regenerated with
RR (https://github.com/GuntherRademacher/rr). RR only understands W3C-style EBNF, so
DHParser's ``~`` (insignificant whitespace) is dropped from a temporary copy of the grammar.
For the same reason, the grammar must not use DHParser's ``/regex/`` literals.

Usage (from anywhere, on Windows or Linux):

    python grammar/update_parser.py
    python grammar/update_parser.py --rr path/to/rr.war [--java path/to/java]
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from DHParser.configuration import access_presets, finalize_presets, set_preset_value
from DHParser.dsl import compile_on_disk

GRAMMAR_DIR = Path(__file__).resolve().parent
EBNF_PATH = GRAMMAR_DIR / "lcma_standard.ebnf"
GENERATED_PARSER = GRAMMAR_DIR / "lcma_standardParser.py"
PACKAGE_PARSER = GRAMMAR_DIR.parent / "src" / "musicalform" / "cli" / "lcma_standardParser.py"
DIAGRAM_INDEX = GRAMMAR_DIR / "index.md"
DIAGRAM_DIR = GRAMMAR_DIR / "diagram"


def update_parser() -> int:
    # same configuration as DHParser.scripts.dhparser.main(), the entry point of the `dhparser` command
    access_presets()
    set_preset_value("syntax_variant", "heuristic")
    finalize_presets()

    if not GENERATED_PARSER.exists() and PACKAGE_PARSER.exists():
        shutil.copy2(PACKAGE_PARSER, GENERATED_PARSER)

    errors = compile_on_disk(str(EBNF_PATH))
    if errors:
        print("\n".join(str(err) for err in errors))
        return 1
    print(f"{EBNF_PATH.name} successfully compiled to {GENERATED_PARSER.name}")

    shutil.move(str(GENERATED_PARSER), str(PACKAGE_PARSER))
    print(f"Moved {GENERATED_PARSER.name} to {PACKAGE_PARSER}")
    return 0


def ebnf_for_rr(ebnf: str) -> str:
    """Convert the DHParser grammar into W3C-style EBNF as expected by RR.

    Removes DHParser's ``~`` (insignificant whitespace) everywhere except in comments,
    string literals and character classes, e.g. the one of MaterialOperator.
    """
    out = []
    i = 0
    while i < len(ebnf):
        c = ebnf[i]
        if ebnf.startswith("/*", i):  # comment
            j = ebnf.index("*/", i + 2) + 2
        elif c in "'\"":  # string literal
            j = ebnf.index(c, i + 1) + 1
        elif c == "[":  # character class
            j = ebnf.index("]", i + 2) + 1
        elif c == "~":  # DHParser's insignificant whitespace
            i += 1
            continue
        else:
            j = i + 1
        out.append(ebnf[i:j])
        i = j
    return "".join(out)


def update_diagrams(rr: Path, java: str) -> int:
    """Regenerate index.md and diagram/*.png from lcma_standard.ebnf using RR."""
    rr_command = [java, "-jar", str(rr)] if rr.suffix in (".war", ".jar") else [str(rr)]
    with tempfile.TemporaryDirectory() as tmp:
        grammar = Path(tmp) / EBNF_PATH.name
        zip_path = Path(tmp) / "diagrams.zip"
        grammar.write_text(ebnf_for_rr(EBNF_PATH.read_text(encoding="utf-8")), encoding="utf-8")
        result = subprocess.run(
            [*rr_command, "-md", "-png", "-noembedded", "-enc:UTF-8", f"-out:{zip_path}", str(grammar)]
        )
        if result.returncode != 0 or not zip_path.exists():
            print(f"RR failed (exit code {result.returncode}), diagrams were not updated.")
            return 1
        # remove old diagrams so that those of deleted rules do not linger
        shutil.rmtree(DIAGRAM_DIR, ignore_errors=True)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(GRAMMAR_DIR)
    print(f"Updated railroad diagrams in {DIAGRAM_INDEX.name} and {DIAGRAM_DIR.name}/")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--rr",
        type=Path,
        metavar="PATH",
        help="RR executable or rr.war; if given, also regenerate the railroad diagrams",
    )
    parser.add_argument(
        "--java",
        default="java",
        metavar="PATH",
        help="Java (>= 11) executable used to run rr.war (default: java on PATH)",
    )
    args = parser.parse_args()

    status = update_parser()
    if status == 0 and args.rr is not None:
        status = update_diagrams(args.rr, args.java)
    return status


if __name__ == "__main__":
    sys.exit(main())
