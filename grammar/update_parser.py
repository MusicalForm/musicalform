#!/usr/bin/env python3
"""Regenerate the LCMA parser from lcma_standard.ebnf and install it into the musicalform package.

Equivalent to running ``dhparser lcma_standard.ebnf`` in this directory (it calls the same
``DHParser.dsl.compile_on_disk`` function as the ``dhparser`` command) and then moving the
generated lcma_standardParser.py to src/musicalform/cli/, overwriting the existing one.

DHParser preserves the editable sections (preprocessor, AST transformations, compiler) of an
existing lcma_standardParser.py next to the grammar. Since this script moves that file away,
the package's copy is placed here first if none exists, so that those sections survive.

Usage (from anywhere, on Windows or Linux):

    python grammar/update_parser.py
"""

import shutil
import sys
from pathlib import Path

from DHParser.configuration import access_presets, finalize_presets, set_preset_value
from DHParser.dsl import compile_on_disk

GRAMMAR_DIR = Path(__file__).resolve().parent
EBNF_PATH = GRAMMAR_DIR / "lcma_standard.ebnf"
GENERATED_PARSER = GRAMMAR_DIR / "lcma_standardParser.py"
PACKAGE_PARSER = GRAMMAR_DIR.parent / "src" / "musicalform" / "cli" / "lcma_standardParser.py"


def main() -> int:
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


if __name__ == "__main__":
    sys.exit(main())
