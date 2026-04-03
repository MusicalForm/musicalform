"""Core domain model for musical form annotation labels."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Self, Set, Tuple
from warnings import warn

from musicalform.enums import (
    MAIN_TO_SUBTYPES,
    CertaintyName,
    FunctionSpecificity,
    MainType,
    MaterialOperator,
    PlaceholderName,
    ReferenceSentinel,
    SpecificFunctionName,
    SubType,
    UnitName,
)
from musicalform.utils import (
    check_for_unhandled_keys,
    compact_repr,
    concatenate_regex_results,
    parse_expression_as_dict,
)

# ---------------------------------------------------------------------------
# Abstract base classes
# ---------------------------------------------------------------------------


class FormalFunction(ABC):

    @abstractmethod
    def specificity(self) -> FunctionSpecificity:
        raise NotImplementedError


class References(ABC):
    pass


class ReferencingLabel(ABC):  # noqa: B024
    material: Optional[MaterialReferences] = None

    @classmethod
    def from_parse(
        cls,
        material_references: Optional[dict] = None,
        shorthand: Optional[SingleReference] = None,
        transformational: bool = False,
        **kwargs,
    ) -> Self:
        """Instantiate from "MaterialBrackets" dict and/or shorthand (=anonymous reference)."""
        if material_references is None and shorthand is None:
            return cls(**kwargs)
        material_refs = _parse_material_brackets(
            material_references,
            shorthand=shorthand,
            transformational=transformational,
        )
        return cls(**kwargs, material=material_refs)


# ---------------------------------------------------------------------------
# Concrete function classes
# ---------------------------------------------------------------------------


@compact_repr
@dataclass
class SingleFunction(FormalFunction):
    name: SpecificFunctionName | UnitName
    notional: bool = False  # "function"
    crossing_rightward: bool = False  # function /

    @classmethod
    def from_name(
        cls,
        name: SpecificFunctionName | UnitName,
        notional=False,
        crossing_rightward=False,
        cardinality=None,
    ) -> SpecificFunction | GenericFunction:
        """Dispatch to the appropriate subclass based on the type of the name.
        Cardinality is only applicable to generic functions and must be None for specific functions.
        """
        if isinstance(name, SpecificFunctionName):
            if cardinality is not None:
                raise ValueError(f"Cardinality is not applicable to specific functions. Got {cardinality=}")
            return SpecificFunction(name=name, notional=notional, crossing_rightward=crossing_rightward)
        elif isinstance(name, UnitName):
            return GenericFunction(
                name=name,
                notional=notional,
                crossing_rightward=crossing_rightward,
                cardinality=cardinality,
            )
        else:
            raise ValueError(f"Name must be either SpecificFunctionName or UnitName. Got {name!r} of type {type(name)}")


@compact_repr
@dataclass
class SpecificFunction(SingleFunction):
    name: SpecificFunctionName

    @property
    def specificity(self) -> FunctionSpecificity:
        return FunctionSpecificity.specific


@compact_repr
@dataclass
class GenericFunction(SingleFunction):
    """Inheritance only in terms of attributes, not in terms of the music-theoretical concept."""

    name: UnitName
    cardinality: Optional[int] = None  # e.g. 1st unit => 1

    @property
    def specificity(self) -> FunctionSpecificity:
        return FunctionSpecificity.generic


@dataclass
class FunctionalTransformation(FormalFunction):
    source: SpecificFunction | GenericFunction
    target: SpecificFunction | GenericFunction

    @property
    def specificity(self) -> Tuple[FunctionSpecificity, FunctionSpecificity]:
        return self.source.specificity, self.target.specificity


# ---------------------------------------------------------------------------
# Formal type
# ---------------------------------------------------------------------------


@compact_repr
@dataclass
class FormalType:
    main_type: MainType
    sub_type: Optional[SubType] = None
    notional: bool = False  # "type"

    @classmethod
    def from_parse(cls, parse: Optional[dict | list]) -> Optional[FormalType]:
        if parse is None:
            return None
        if isinstance(parse, dict):
            type_name = parse.pop("FormalType")
            check_for_unhandled_keys(parse)
            main, sub = _parse_type_name(type_name)
            return cls(main_type=main, sub_type=sub, notional=False)
        main, sub = None, None
        for thing in parse:
            # 3 things: '"', <TypeName>, '"'
            match thing:
                case ["FormalType", type_name]:
                    main, sub = _parse_type_name(type_name)
                case [":Text", '"']:
                    pass
                case _:
                    warn(
                        f"Encountered unknown thing in formal type: {thing!r}",
                        UserWarning,
                    )
        return cls(main_type=main, sub_type=sub, notional=True)

    def __repr__(self) -> str:
        repr = f"FormalType({self.main_type}"
        if self.sub_type:
            repr += f".{self.sub_type}"
        repr += ")"
        return repr


# ---------------------------------------------------------------------------
# References
# ---------------------------------------------------------------------------


@dataclass
class SingleReference(References):
    reference: Optional[str | ReferenceSentinel] = None
    operators: Set[MaterialOperator] = field(default_factory=set)

    @classmethod
    def from_parse(cls, parse: dict):
        if parse is None:
            return None
        name = parse.pop("Name", ReferenceSentinel.previous)
        operator_chars = parse.pop("MaterialOperators", [])
        operators = _parse_material_operator_chars(operator_chars)
        return cls(reference=name, operators=operators)


@compact_repr
@dataclass
class MaterialReferences(References):
    """One or several material references, possibly with operators."""

    references: Tuple[SingleReference, ...]
    unordered: bool = False  # if True, this is considered a non-repeating set

    @classmethod
    def from_parse(cls, parse: Optional[list], shorthand: Optional[SingleReference]) -> Optional[MaterialReferences]:
        if parse is None and shorthand is None:
            return None
        if shorthand and parse:
            raise ValueError("Shorthand and material brackets cannot be combined.")
        if shorthand:
            return cls(references=(shorthand,))
        for thing in parse:
            match thing:
                case ["MaterialPositions", positions]:
                    return _parse_material_positions(positions)
                case [":Text", _] | [":Whitespace", _]:
                    pass
                case _:
                    warn(
                        f"Encountered unknown thing in material brackets: {thing!r}",
                        UserWarning,
                    )
        return None


@dataclass
class TransformationalReferences(References):
    source_references: Optional[MaterialReferences] = None
    target_references: Optional[MaterialReferences] = None

    @classmethod
    def from_parse(
        cls, parse: Optional[list], shorthand: Optional[tuple]
    ) -> Optional[TransformationalReferences | MaterialReferences]:
        if parse is None and shorthand is None:
            return None
        if parse is None and shorthand is not None:
            source_short, target_short = shorthand
            return cls(
                source_references=(MaterialReferences(references=(source_short,)) if source_short else None),
                target_references=(MaterialReferences(references=(target_short,)) if target_short else None),
            )
        for thing in parse:
            match thing:
                case ["MaterialPositions", positions]:
                    if shorthand is not None:
                        source_short, target_short = shorthand
                        if source_short or target_short:
                            raise ValueError("Shorthand and material brackets cannot be combined.")
                    return _parse_transformational_positions(positions)
                case [":Text", _] | [":Whitespace", _]:
                    pass
                case _:
                    warn(
                        f"Encountered unknown thing in material brackets: {thing!r}",
                        UserWarning,
                    )
        return None


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------


@compact_repr
@dataclass
class PlaceholderLabel(ReferencingLabel):
    name: PlaceholderName
    material: Optional[MaterialReferences] = None

    @classmethod
    def from_parse(cls, parse: dict):
        name = PlaceholderName(parse.pop("Placeholder"))
        shorthand = parse.pop("Shorthand", None)
        shorthand_ref = SingleReference.from_parse(shorthand)
        material_references = parse.pop("MaterialBrackets", None)
        check_for_unhandled_keys(parse)
        if material_references or shorthand_ref:
            return super().from_parse(
                material_references=material_references,
                shorthand=shorthand_ref,
                transformational=False,
                name=name,
            )
        return cls(name)


@compact_repr(certainty=CertaintyName.default)
@dataclass
class FormLabel(ReferencingLabel):
    function: FormalFunction
    type: Optional[FormalType] = None
    material: Optional[MaterialReferences] = None
    certainty: CertaintyName = CertaintyName.default

    @classmethod
    def from_parse(cls, parse: dict):
        form_dict = parse["Form"]
        function, shorthand = _parse_function_label(form_dict.pop("FunctionLabel"))
        certainty = CertaintyName(form_dict.pop("Certainty", CertaintyName.default))
        formal_type = FormalType.from_parse(form_dict.pop("TypeExp", None))
        material_references = parse.pop("MaterialBrackets", None)
        check_for_unhandled_keys(form_dict)
        return super().from_parse(
            material_references=material_references,
            shorthand=shorthand,
            transformational=isinstance(function, FunctionalTransformation),
            function=function,
            type=formal_type,
            certainty=certainty,
        )


@dataclass
class AnnotationLabel:
    name: Optional[str]
    form_labels: List[FormLabel] = field(default_factory=list)

    @classmethod
    def from_string(cls, label: str) -> Self:
        tree_dict = parse_expression_as_dict(label)
        return cls.from_parse(tree_dict)

    @classmethod
    def from_parse(cls, parse: dict) -> Self:
        try:
            label = parse["Label"]
        except KeyError:
            raise ValueError(parse)
        name = None
        labels = []
        if "Name" in label:
            name = _parse_name(label.pop("Name"))
        if isinstance(label, dict):
            if "PlaceholderLabel" in label:
                labels.append(PlaceholderLabel.from_parse(label.pop("PlaceholderLabel")))
            else:
                labels.append(FormLabel.from_parse(label.pop("FormLabel")))
            check_for_unhandled_keys(label)
        else:
            for thing in label:
                match thing:
                    case ["Name", name_list]:
                        name = _parse_name(name_list)
                    case ["FormLabel", label_dict]:
                        labels.append(FormLabel.from_parse(label_dict))
                    case ["Placeholder", placeholder_dict]:
                        labels.append(PlaceholderLabel.from_parse(placeholder_dict))
                    case [":Text", _] | [":Whitespace", _]:
                        pass
                    case _:
                        warn(f"Encountered unknown thing: {thing!r}", UserWarning)
        return cls(name=name, form_labels=labels)


# ---------------------------------------------------------------------------
# Internal parsing helpers (module-private)
# These translate the DHParser JSON-dict output into musicalform objects.
# They are called from the from_parse class methods above.
# ---------------------------------------------------------------------------


def _parse_function_name(
    function_name: dict,
) -> Tuple[SpecificFunctionName | UnitName, Optional[int]]:
    if "SpecificFunction" in function_name:
        return SpecificFunctionName(function_name["SpecificFunction"]), None
    elif "GenericFunction" in function_name:
        generic_function = function_name["GenericFunction"]
        name = UnitName(generic_function.pop("Unit"))
        cardinality = generic_function.pop("Cardinality", None)
        if cardinality is not None:
            # has the shape "1st", or "2nd", ... "9th"
            cardinality = int(cardinality[0])
        check_for_unhandled_keys(generic_function)
        return name, cardinality
    else:
        warn(f"Encountered unknown function type: {function_name!r}", UserWarning)
        return None, None


def _parse_function(
    function: dict | list,
) -> SpecificFunction | GenericFunction:
    """Can be either function or "function" (for notional function attribution)."""
    if isinstance(function, dict):
        function_name = function.pop("FunctionName")
        check_for_unhandled_keys(function)
        name, cardinality = _parse_function_name(function_name)
        return SingleFunction.from_name(name=name, notional=False, cardinality=cardinality)
    name, cardinality = None, None
    for thing in function:
        # 3 things: '"', <FunctionName>, '"'
        match thing:
            case ["FunctionName", function_name]:
                name, cardinality = _parse_function_name(function_name)
            case [":Text", '"']:
                pass
            case _:
                warn(f"Encountered unknown thing in function: {thing!r}", UserWarning)
    return SingleFunction.from_name(name=name, notional=True, cardinality=cardinality)


def _parse_function_expr(
    function_expr: dict,
) -> Tuple[SpecificFunction | GenericFunction, Optional[SingleReference]]:
    function = function_expr.pop("Function")
    formal_function = _parse_function(function)
    shorthand = function_expr.pop("Shorthand", None)
    shorthand_ref = SingleReference.from_parse(shorthand)
    check_for_unhandled_keys(function_expr)
    return formal_function, shorthand_ref


TransformationalShorthand = Tuple[SingleReference, SingleReference]


def _parse_function_label(
    parse: dict | list,
) -> Tuple[FormalFunction, Optional[SingleReference]] | Tuple[FunctionalTransformation, TransformationalShorthand]:
    if isinstance(parse, dict):
        function_expr = parse.pop("FunctionExpr")
        check_for_unhandled_keys(parse)
        return _parse_function_expr(function_expr)
    functions, shorthands = [], []
    operator = None
    for thing in parse:
        match thing:
            case ["FunctionExpr", function_expr]:
                function, shorthand = _parse_function_expr(function_expr)
                functions.append(function)
                shorthands.append(shorthand)
            case ["Combinator", combinator]:
                operator = combinator
            case [":Text", _] | [":Whitespace", _]:
                pass
            case _:
                warn(
                    f"Encountered unknown thing in function label: {thing!r}",
                    UserWarning,
                )
    if len(functions) == 1:
        function = functions[0]
        assert operator == "/"
        function.crossing_rightward = True
        return function, shorthands[0]
    # interpret as transformation from first to second function
    assert len(functions) == 2
    assert operator == ">"
    transformation = FunctionalTransformation(source=functions[0], target=functions[1])
    return transformation, tuple(shorthands)


def _parse_name(name_list: str | list) -> str:
    if isinstance(name_list, str):
        return name_list.strip()
    return concatenate_regex_results(name_list)


def _parse_type_name(type_name: str) -> Tuple[MainType, Optional[SubType]]:
    from musicalform.utils import concatenate_regex_results as _crr

    if isinstance(type_name, list):
        # e.g.: [[':Text', 'repeated'], [':Text', '_'], ['Unit', 'section']]
        type_name = _crr(type_name)
    elif isinstance(type_name, dict):
        type_name = "repeated_" + type_name["Unit"]
    elif "." in type_name:
        main_str, sub_str = type_name.split(".", 1)
        main = MainType(main_str)
        sub = SubType(sub_str)
        if main not in MAIN_TO_SUBTYPES:
            raise ValueError(f"Main type {main} does not have any subtypes, but got subtype {sub}")
        elif sub not in MAIN_TO_SUBTYPES[main]:
            raise ValueError(
                f"Subtype {sub} is not valid for main type {main}. " f"Valid subtypes are: {MAIN_TO_SUBTYPES[main]}"
            )
        return main, sub
    return MainType(type_name), None


def _parse_material_operator_chars(operator_chars: list | str) -> Set[MaterialOperator]:
    """For simplicity, the standard allows for any combination of the operators [°, &, +, ~, *, !, ^].
    However, each operator is taken into account only once and ** needs to be extracted before * (although both
    should not appear at the same time in the first place).
    """
    import re

    if not operator_chars:
        return set()
    if isinstance(operator_chars, str):
        operators_string = operator_chars
    else:
        from musicalform.utils import concatenate_regex_results

        operators_string = concatenate_regex_results(operator_chars)

    # Symbol map in alphabetical order
    symbol_map = {
        "°": MaterialOperator.adaptation,
        "&": MaterialOperator.combination,
        ",": MaterialOperator.concatenation,
        "+": MaterialOperator.extension,
        "**": MaterialOperator.interpolation,
        "~": MaterialOperator.ornamentation,
        "*": MaterialOperator.partial,
        "!": MaterialOperator.repetition,
        "^": MaterialOperator.transposition,
    }

    # Sort by length descending to match ** before *
    sorted_symbols = sorted(symbol_map.keys(), key=len, reverse=True)
    pattern = "|".join(re.escape(symbol) for symbol in sorted_symbols)
    matches = re.findall(pattern, operators_string)
    return set(symbol_map[match] for match in matches)


def _parse_material_concatenation(concat_list: list) -> Tuple[SingleReference, ...]:
    refs = []
    for thing in concat_list:
        match thing:
            case ["Entry", entry_dict]:
                refs.append(SingleReference.from_parse(entry_dict))
            case [":Text", _] | [":Whitespace", _]:
                pass
            case _:
                warn(
                    f"Encountered unknown thing in material concatenation: {thing!r}",
                    UserWarning,
                )
    return tuple(refs)


def _parse_material_ref(material_ref: dict | list) -> MaterialReferences:
    if isinstance(material_ref, dict):
        if "Entry" in material_ref:
            entry = material_ref.pop("Entry", None)
            ref = SingleReference.from_parse(entry)
            check_for_unhandled_keys(material_ref)
            return MaterialReferences(references=(ref,))
        elif "Concatenation" in material_ref:
            refs = _parse_material_concatenation(material_ref.pop("Concatenation"))
            check_for_unhandled_keys(material_ref)
            return MaterialReferences(references=refs)
    # list: bracket-wrapped or paren-wrapped
    unordered = False
    refs = ()
    for thing in material_ref:
        match thing:
            case ["Concatenation", concat_list]:
                refs = _parse_material_concatenation(concat_list)
            case [":Text", "(" | ")"]:
                unordered = True
            case [":Text", _] | [":Whitespace", _]:
                pass
            case _:
                warn(f"Encountered unknown thing in material ref: {thing!r}", UserWarning)
    return MaterialReferences(references=refs, unordered=unordered)


def _parse_material_positions(
    positions: dict | list,
) -> Optional[MaterialReferences]:
    """For a single function: only a single MaterialRef without positional syntax."""
    if isinstance(positions, list):
        raise ValueError("Two material positions are not allowed for a single function.")
    if "SourceOnly" in positions or "TargetOnly" in positions:
        raise ValueError("Positional material references are not allowed for a single function.")
    if "MaterialRef" in positions:
        return _parse_material_ref(positions["MaterialRef"])
    return None


def _parse_transformational_positions(
    positions: dict | list,
) -> Optional[TransformationalReferences | MaterialReferences]:
    """For a functional transformation: disambiguate between positions and overrides."""
    if isinstance(positions, list):
        # two explicit MaterialRef positions
        refs = []
        for thing in positions:
            match thing:
                case ["MaterialRef", ref_data]:
                    refs.append(_parse_material_ref(ref_data))
                case [":Text", _] | [":Whitespace", _]:
                    pass
                case _:
                    warn(
                        f"Encountered unknown thing in material positions: {thing!r}",
                        UserWarning,
                    )
        return TransformationalReferences(
            source_references=refs[0] if len(refs) > 0 else None,
            target_references=refs[1] if len(refs) > 1 else None,
        )
    if "SourceOnly" in positions:
        return TransformationalReferences(
            source_references=_parse_material_ref(positions["SourceOnly"]["MaterialRef"]),
            target_references=None,
        )
    if "TargetOnly" in positions:
        return TransformationalReferences(
            source_references=None,
            target_references=_parse_material_ref(positions["TargetOnly"]["MaterialRef"]),
        )
    if "MaterialRef" not in positions:
        return None
    material_ref = positions["MaterialRef"]
    # bare concatenation: reinterpret based on entry count
    if isinstance(material_ref, dict) and "Concatenation" in material_ref:
        entries = [thing for thing in material_ref["Concatenation"] if thing[0] == "Entry"]
        if len(entries) == 2:
            source_single = SingleReference.from_parse(entries[0][1])
            target_single = SingleReference.from_parse(entries[1][1])
            return TransformationalReferences(
                source_references=MaterialReferences(references=(source_single,)),
                target_references=MaterialReferences(references=(target_single,)),
            )
        raise ValueError(
            f"Bare concatenation with {len(entries)} entries is not allowed " f"for a functional transformation."
        )
    # bracket/paren-wrapped or single entry: override to MaterialReferences
    return _parse_material_ref(material_ref)


MaterialPosition = Optional[SingleReference]


def _parse_material_brackets(
    material_brackets: Optional[dict | list],
    shorthand: MaterialPosition | Tuple[MaterialPosition, MaterialPosition],
    transformational: bool = False,
) -> Optional[MaterialReferences]:
    if transformational:
        return TransformationalReferences.from_parse(material_brackets, shorthand)
    else:
        return MaterialReferences.from_parse(material_brackets, shorthand)
