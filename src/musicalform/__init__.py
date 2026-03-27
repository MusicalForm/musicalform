"""musicalform: A Python library for representing and validating musical form annotation labels."""

try:
    from importlib.metadata import version as _get_version

    __version__ = _get_version("musicalform")
except Exception:
    __version__ = "0.1.0"  # fallback for development

from musicalform.core import (
    AnnotationLabel,
    FormalFunction,
    FormalType,
    FormLabel,
    FunctionalTransformation,
    GenericFunction,
    MaterialReferences,
    PlaceholderLabel,
    References,
    ReferencingLabel,
    SingleFunction,
    SingleReference,
    SpecificFunction,
    TransformationalReferences,
)
from musicalform.enums import (
    MAIN_TO_SUBTYPES,
    CertaintyName,
    FancyStrEnum,
    FunctionSpecificity,
    MainType,
    MaterialOperator,
    PlaceholderName,
    ReferenceSentinel,
    SpecificFunctionName,
    SubType,
    UnitName,
)

__all__ = [
    "__version__",
    # enums
    "FancyStrEnum",
    "SpecificFunctionName",
    "UnitName",
    "FunctionSpecificity",
    "MainType",
    "SubType",
    "MAIN_TO_SUBTYPES",
    "MaterialOperator",
    "PlaceholderName",
    "CertaintyName",
    "ReferenceSentinel",
    # core
    "FormalFunction",
    "SingleFunction",
    "SpecificFunction",
    "GenericFunction",
    "FunctionalTransformation",
    "FormalType",
    "References",
    "SingleReference",
    "MaterialReferences",
    "TransformationalReferences",
    "ReferencingLabel",
    "PlaceholderLabel",
    "FormLabel",
    "AnnotationLabel",
]
