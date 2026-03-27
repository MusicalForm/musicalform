"""Basic smoke tests for the musicalform library."""

import pytest

from musicalform.core import FormalType, GenericFunction, SingleFunction, SpecificFunction
from musicalform.enums import (
    CertaintyName,
    FunctionSpecificity,
    MainType,
    MaterialOperator,
    PlaceholderName,
    SpecificFunctionName,
    SubType,
    UnitName,
)


class TestFancyStrEnum:
    def test_alias_lookup(self):
        assert SpecificFunctionName("bi") == SpecificFunctionName.basic_idea

    def test_canonical_lookup(self):
        assert SpecificFunctionName("basic_idea") == SpecificFunctionName.basic_idea

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            SpecificFunctionName("not_a_function")

    def test_material_operator_symbol(self):
        assert MaterialOperator("!") == MaterialOperator.repetition
        assert MaterialOperator("^") == MaterialOperator.transposition

    def test_placeholder_symbol(self):
        assert PlaceholderName("%") == PlaceholderName.repeat

    def test_certainty_symbol(self):
        assert CertaintyName("?") == CertaintyName.uncertain


class TestSingleFunction:
    def test_from_name_specific(self):
        fn = SingleFunction.from_name(SpecificFunctionName.basic_idea)
        assert isinstance(fn, SpecificFunction)
        assert fn.specificity == FunctionSpecificity.specific

    def test_from_name_generic(self):
        fn = SingleFunction.from_name(UnitName.phrase, cardinality=2)
        assert isinstance(fn, GenericFunction)
        assert fn.cardinality == 2
        assert fn.specificity == FunctionSpecificity.generic

    def test_cardinality_disallowed_for_specific(self):
        with pytest.raises(ValueError):
            SingleFunction.from_name(SpecificFunctionName.coda, cardinality=1)


class TestFormalType:
    def test_simple_main_type(self):
        ft = FormalType(main_type=MainType.sentence)
        assert ft.main_type == MainType.sentence
        assert ft.sub_type is None

    def test_maintype_alias(self):
        assert MainType("sent") == MainType.sentence

    def test_subtype_valid(self):
        ft = FormalType(main_type=MainType.ternary, sub_type=SubType.da_capo)
        assert ft.sub_type == SubType.da_capo
