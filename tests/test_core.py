"""Basic smoke tests for the musicalform library."""

import pytest

from musicalform.core import (
    AnnotationLabel,
    FormalType,
    FunctionalFusion,
    FunctionalTransformation,
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


class TestCombinators:
    def test_fusion(self):
        function = AnnotationLabel.from_string("cont/codetta")[0].function
        assert isinstance(function, FunctionalFusion)
        assert function.first.name == SpecificFunctionName.continuation_idea
        assert function.second.name == SpecificFunctionName.codetta

    def test_transformation(self):
        function = AnnotationLabel.from_string("cont>codetta")[0].function
        assert isinstance(function, FunctionalTransformation)

    def test_fusion_with_subsequent_label(self):
        form_label = AnnotationLabel.from_string("cont/")[0]
        assert isinstance(form_label.function, SpecificFunction)
        assert form_label.crossing_rightward
        assert not form_label.transforming_rightward

    def test_transformation_into_subsequent_label(self):
        form_label = AnnotationLabel.from_string("cont>")[0]
        assert isinstance(form_label.function, SpecificFunction)
        assert form_label.transforming_rightward
        assert not form_label.crossing_rightward

    def test_combinator_after_type(self):
        form_label = AnnotationLabel.from_string("conti|modseq /")[0]
        assert isinstance(form_label.function, SpecificFunction)
        assert form_label.type.main_type == MainType.model_sequence
        assert form_label.crossing_rightward

    def test_binary_function_with_subsequent_label(self):
        form_label = AnnotationLabel.from_string("mod > seq|sent [a,b] /")[0]
        assert isinstance(form_label.function, FunctionalTransformation)
        assert form_label.type.main_type == MainType.sentence
        assert form_label.crossing_rightward
        assert not form_label.transforming_rightward

    @pytest.mark.parametrize(
        "label, expected",
        [
            ("cont/codetta", "cont / cdta"),
            ("cont / codetta [a,b]", "cont / cdta [a,b]"),
            ("cont>codetta", "cont > cdta"),
            ("cont/", "cont /"),
            ("cont>", "cont >"),
            ("conti|modseq /", "cont|modseq /"),
            ("conti|modseq >", "cont|modseq >"),
            ("cont [a] >", "cont [a] >"),
            ("mod > seq|sent [a,b] /", "mod > seq|sent [a,b] /"),
        ],
    )
    def test_rendering(self, label, expected):
        assert str(AnnotationLabel.from_string(label)) == expected


class TestMaterialCombination:
    def test_placeholder_with_combination(self):
        material = AnnotationLabel.from_string("% [B&A']")[0].material
        assert material.combined
        assert [ref.reference for ref in material.references] == ["B", "A'"]

    def test_combination_as_transformation_source(self):
        material = AnnotationLabel.from_string("mod > seq [a&b, c]")[0].material
        assert material.source_references.combined
        assert not material.target_references.combined

    @pytest.mark.parametrize(
        "label, expected",
        [
            ("% [B&A']", "% [B&A']"),
            ("%[B & A']", "% [B&A']"),
            ("x [a&b*&c]", "x [a&b*&c]"),
            ("mod > seq [a&b, c]", "mod > seq [a&b,c]"),
        ],
    )
    def test_rendering(self, label, expected):
        assert str(AnnotationLabel.from_string(label)) == expected
