"""Basic smoke tests for the musicalform library."""

import pytest

from musicalform.core import (
    AnnotationLabel,
    FormalType,
    GenericFunction,
    SingleFunction,
    SingleReference,
    SpecificFunction,
    _parse_material_operator_chars,
)
from musicalform.enums import (
    MATERIAL_OPERATOR_ORDER,
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


class TestMaterialOperatorOrder:
    def test_order_covers_all_operators(self):
        assert set(MATERIAL_OPERATOR_ORDER) == set(MaterialOperator)
        assert len(MATERIAL_OPERATOR_ORDER) == len(set(MATERIAL_OPERATOR_ORDER))

    def test_parsed_operators_are_canonical(self):
        ops = _parse_material_operator_chars("°+**~!!^*")
        assert ops == tuple(sorted(ops, key=MATERIAL_OPERATOR_ORDER.index))
        assert SingleReference(reference="a", operators=ops).to_label() == "a!^***+~°"

    def test_operators_given_as_set_are_sorted(self):
        ref = SingleReference(
            reference="a",
            operators={MaterialOperator.adaptation, MaterialOperator.extension, MaterialOperator.partial},
        )
        assert ref.to_label() == "a*+°"

    @pytest.mark.parametrize(
        "label, expected",
        [
            ("cad [a°+]", "cad [a+°]"),
            ("cad [A+°]", "cad [A+°]"),
            ("seq!!* > cad", "seq > cad [_!*,]"),
            ("seq^*", "seq [_^*]"),
        ],
    )
    def test_label_rendering_is_canonical(self, label, expected):
        assert str(AnnotationLabel.from_string(label)) == expected
