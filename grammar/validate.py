"""Validate LCMA form-annotation labels against the current grammar.

This script is the thin wrapper kept in the grammar/ directory for backward
compatibility. All domain objects (dataclasses, enumerations) come from
the musicalform library.
"""

from __future__ import annotations

# All domain objects now come from the musicalform library.
from musicalform import (  # noqa: F401 — re-exported for backwards compatibility
    MAIN_TO_SUBTYPES,
    AnnotationLabel,
    CertaintyName,
    FancyStrEnum,
    FormalType,
    FormLabel,
    FunctionalTransformation,
    FunctionSpecificity,
    GenericFunction,
    MainType,
    MaterialOperator,
    MaterialReferences,
    PlaceholderLabel,
    PlaceholderName,
    References,
    ReferenceSentinel,
    ReferencingLabel,
    SingleFunction,
    SingleReference,
    SpecificFunction,
    SpecificFunctionName,
    SubType,
    TransformationalReferences,
    UnitName,
)

# The full CLI and parsing pipeline comes from musicalform.cli.validate.
from musicalform.cli.validate import (  # noqa: F401 — re-exported for backwards compatibility
    _resolve_single_output,
    _validate_and_report,
    is_valid_json_format,
    json_to_dataframe,
    main,
    parse_args,
    parse_csv_file,
    parse_expression,
    parse_expression_as,
    parse_expression_as_dict,
    parse_expression_as_objects,
    parse_file,
    parse_file_as,
    parse_file_as_dict,
    parse_file_as_objects,
    parse_tree,
    process_json_directory,
    process_json_file,
    resolve_output_path,
    run,
)

if __name__ == "__main__":
    run()
