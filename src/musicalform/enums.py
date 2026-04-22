"""Enumerations for the musicalform domain model."""

from __future__ import annotations

from collections import defaultdict
from enum import StrEnum, auto


class FancyStrEnum(StrEnum):
    """A StrEnum with support for abbreviation aliases and flexible instantiation.

    Features:
        * Can be instantiated from any alias: FancyStrEnum("abbr") == FancyStrEnum.abbreviation
        * list(FancyStrEnum) returns only non-aliases (canonical members)
        * FancyStrEnum.get_abbreviations() returns a mapping from names to abbreviations

    Example:
        class Vocabulary(FancyStrEnum):
            abbreviation = auto()  # assigns the name as value (lowercase per StrEnum)
            abbr = abbreviation    # alias 1
            abb = abbreviation     # alias 2
    """

    @classmethod
    def _missing_(cls, value: object) -> "FancyStrEnum | None":
        """Allow instantiation from values, including aliases.

        Args:
            value: The value or name string to look up.

        Returns:
            The corresponding enum member, or None if not found.

        Raises:
            ValueError: If the value does not match any member or alias.
        """
        if isinstance(value, str):
            lower_value = value.lower()
            if lower_value in cls.__members__:
                name = cls.__members__[lower_value]
                return cls(name)
        abbrv = cls.get_abbreviations(string=True)
        raise ValueError(f"'{value}' is not a valid {cls.__name__}. Available values are: {abbrv}")

    @classmethod
    def get_abbreviations(cls, string: bool = False) -> dict[str, list[str]] | str:
        """Returns a mapping from enum names/values to abbreviated alias values.

        Args:
            string: If True, return a formatted string instead of a dict.

        Returns:
            A dict mapping canonical names to lists of aliases, or a formatted string.
        """
        name2values: dict[str, list[str]] = defaultdict(list)
        for value, name in cls.__members__.items():
            name2values[name].append(value)
        abbreviations: dict[str, list[str]] = {}
        for name, values in name2values.items():
            # Sort by length descending, skip the first (canonical name)
            abbreviations[name] = sorted(values, key=lambda x: len(x), reverse=True)[1:]
        if not string:
            return abbreviations
        str_components = []
        for name, values in abbreviations.items():
            if not values:
                str_components.append(name)
                continue
            abbrev_str = ", ".join(values)
            str_components.append(f"{name} ({abbrev_str})")
        return ", ".join(str_components)

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"{self.__class__}.{self.name}"


class SpecificFunctionName(FancyStrEnum):
    antecedent = auto()
    ant = antecedent
    after_the_end = auto()
    ate = after_the_end
    basic_idea = auto()
    bi = basic_idea
    cadential_subphrase = auto()
    cad = cadential_subphrase
    compound_basic_idea = auto()
    cbi = compound_basic_idea
    codetta = auto()
    cdta = codetta
    contrasting_idea = auto()
    ci = contrasting_idea
    closing_theme = auto()
    cls = closing_theme
    coda = auto()
    consequent = auto()
    cons = consequent
    continuation_idea = auto()
    conti = continuation_idea
    continuation = continuation_idea
    cont = continuation
    development_section = auto()
    dev = development_section
    exposition = auto()
    exp = exposition
    fragmentation = auto()
    frag = fragmentation
    introduction = auto()
    intro = introduction
    lead_in = auto()
    lin = lead_in
    model = auto()
    mod = model
    movement = auto()
    mvt = movement
    postcadential = auto()
    pcad = postcadential
    presentation = auto()
    pres = presentation
    primary_theme_zone = auto()
    ptz = primary_theme_zone
    primary_theme = primary_theme_zone
    pt = primary_theme
    recapitulation = auto()
    recap = recapitulation
    ritornello = auto()
    rit = ritornello
    retransition = auto()
    rtr = retransition
    secondary_theme_zone = auto()
    stz = secondary_theme_zone
    secondary_theme = secondary_theme_zone
    st = secondary_theme
    sequence = auto()
    seq = sequence
    transition = auto()
    tr = transition


class UnitName(FancyStrEnum):
    unit = auto()
    x = unit
    part = auto()
    section = auto()
    phrase = auto()
    sub_phrase = auto()
    idea = auto()
    work = auto()
    movement = auto()
    zone = auto()
    theme = auto()
    album = auto()
    song = auto()
    cycle = auto()
    group = auto()


class FunctionSpecificity(FancyStrEnum):
    specific = auto()
    generic = auto()


class MainType(FancyStrEnum):
    hybrid1 = auto()
    hyb1 = hybrid1
    hybrid2 = auto()
    hyb2 = hybrid2
    hybrid3 = auto()
    hyb3 = hybrid3
    hybrid4 = auto()
    hyb4 = hybrid4
    model_sequence = auto()
    modseq = model_sequence
    period = auto()
    pd = period
    # repeated_movement
    repeated_part = auto()
    repeated_section = auto()
    repeated_zone = auto()
    repeated_theme = auto()
    repeated_phrase = auto()
    repeated_subphrase = auto()
    repeated_idea = auto()
    ritornello_form = auto()
    ritornello = ritornello_form
    rondo_form = auto()
    rondo = rondo_form
    sentence = auto()
    sent = sentence
    sequence = auto()
    seq = sequence
    sonata_form = auto()
    sonata = sonata_form
    unary_form = auto()
    unary = unary_form
    simple_binary = auto()
    rounded_binary = auto()
    ternary = auto()


class SubType(FancyStrEnum):
    # simple_binary
    balanced = auto()
    # ternary
    through_composed = auto()
    da_capo = auto()


MAIN_TO_SUBTYPES: dict[MainType, set[SubType]] = {
    MainType.simple_binary: {SubType.balanced},
    MainType.ternary: {SubType.through_composed, SubType.da_capo},
}


class MaterialOperator(FancyStrEnum):
    adaptation = auto()  # $adapt symbol: °
    adapt = adaptation
    augmentation = auto()  # $aug
    aug = augmentation
    combination = auto()  # $comb symbol: &
    comb = combination
    concatenation = auto()  # $conc symbol: ,
    conc = concatenation
    diminution = auto()  # $dim
    dim = diminution
    extension = auto()  # $ext symbol: +
    ext = extension
    interpolation = auto()  # $interp symbol: **
    interp = interpolation
    inversion = auto()  # $inv
    inv = inversion
    ornamentation = auto()  # $orn symbol: ~
    orn = ornamentation
    partial = auto()  # $part symbol: *
    part = partial
    repetition = auto()  # $rep symbol: !
    rep = repetition
    retrograde = auto()  # $retr
    retr = retrograde
    transposition = auto()  # $transp symbol: ^
    transp = transposition
    variation = auto()  # $var
    var = variation

    @classmethod
    def _missing_(cls, value: object):
        """Allow instantiation from symbols or aliases.

        Args:
            value: The value, symbol, or alias string to look up.

        Returns:
            The corresponding enum member, or None if not found.

        Raises:
            ValueError: If the value does not match any member, symbol, or alias.
        """
        symbol_map = {
            "°": cls.adaptation,
            "&": cls.combination,
            ",": cls.concatenation,
            "+": cls.extension,
            "**": cls.interpolation,
            "~": cls.ornamentation,
            "*": cls.partial,
            "!": cls.repetition,
            "^": cls.transposition,
        }
        if isinstance(value, str) and value in symbol_map:
            return symbol_map[value]
        return super()._missing_(value)


class PlaceholderName(FancyStrEnum):
    repeat = auto()

    @classmethod
    def _missing_(cls, value: object):
        """Allow instantiation from symbols or aliases.

        Args:
            value: The value, symbol, or alias string to look up.

        Returns:
            The corresponding enum member, or None if not found.

        Raises:
            ValueError: If the value does not match any member, symbol, or alias.
        """
        symbol_map = {"%": cls.repeat}
        if isinstance(value, str) and value in symbol_map:
            return symbol_map[value]
        return super()._missing_(value)


class CertaintyName(FancyStrEnum):
    default = auto()
    uncertain = auto()

    @classmethod
    def _missing_(cls, value: object):
        """Allow instantiation from symbols or aliases.

        Args:
            value: The value, symbol, or alias string to look up.

        Returns:
            The corresponding enum member, or None if not found.

        Raises:
            ValueError: If the value does not match any member, symbol, or alias.
        """
        symbol_map = {"?": cls.uncertain}
        if isinstance(value, str) and value in symbol_map:
            return symbol_map[value]
        return super()._missing_(value)


class ReferenceSentinel(FancyStrEnum):
    previous = auto()
