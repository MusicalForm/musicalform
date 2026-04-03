"""Utility helpers shared across the musicalform library."""

from __future__ import annotations

import json
from dataclasses import fields
from typing import Tuple
from warnings import warn

from DHParser import RootNode

from musicalform.cli.lcma_standardParser import compile_snippet


def compact_repr(_cls=None, *, filter_none=True, filter_false=True, **kwargs):
    """A class decorator that modifies a dataclass's __repr__ to omit
    attributes based on custom rules. Specify fields that you want to
    omit based on a "value" or on ["value1", "value2"] as kwargs.

    Examples:

        @compact_repr                                   # omits None and False fields
        @compact_repr(filter_false=False)               # omits None fields
        @compact_repr(field_name="default")             # shows only non-default values
        @compact_repr(
            certainty=[
                CertaintyName.normal,
                CertaintyName.high,
            ],
        )                                               # shows only low certainty
    """

    ignore_rules = {}
    for field_name, ignore_values in kwargs.items():
        if isinstance(ignore_values, (list, tuple, set)) and not isinstance(ignore_values, str):
            ignore_rules[field_name] = list(ignore_values)
        else:
            ignore_rules[field_name] = [ignore_values]

    def decorator(cls):
        def custom_repr(self):
            parts = []
            for f in fields(self):
                if not f.repr:
                    continue

                value = getattr(self, f.name)

                # 1. Standard boolean and None filters (using 'is' to avoid matching 0 or empty strings)
                if filter_none and value is None:
                    continue
                if filter_false and value is False:
                    continue

                # 2. Custom kwargs filtering
                if value in ignore_rules.get(f.name, []):
                    continue

                parts.append(f"{f.name}={repr(value)}")

            return f"{self.__class__.__name__}({', '.join(parts)})"

        # Overwrite the default __repr__
        cls.__repr__ = custom_repr
        return cls

    # This allows the decorator to be used with or without parentheses
    if _cls is None:
        return decorator
    else:
        return decorator(_cls)


def concatenate_dict_values_recursively(specs) -> str:
    """Recursively concatenates dict values. Pass dict.values() iterator or some other iterator of
    strings and (nested) dicts."""
    result = ""
    for val in specs:
        if isinstance(val, str):
            result += val
        else:
            # assumes that val is dict
            result += concatenate_dict_values_recursively(val.values())
    return result


def concatenate_regex_results(name_list: list, strip=True) -> str:
    """Processes a list of regEx matches and returns the result.

    Example input:
        [[':RegExp', 'n'],
         [':RegExp', 'a'],
         [':RegExp', 'm'],
         [':RegExp', 'e']]
    """
    if strip:
        return "".join(character.strip() for (_, character) in name_list)
    return "".join(character for (_, character) in name_list)


def check_for_unhandled_keys(dct: dict, ignore_keys=(":Text", ":Whitespace")):
    if ignore_keys:
        if isinstance(ignore_keys, str):
            ignore_keys = {ignore_keys}
        else:
            ignore_keys = set(ignore_keys)
    else:
        ignore_keys = set()
    keys = ", ".join(repr(key) for key in dct.keys() if key not in ignore_keys)
    if keys:
        warn(f"Encountered unhandled keys: {keys!r}\n\t{dct}", UserWarning)


def parse_expression(exp: str, remove_whitespace: bool = True):
    if remove_whitespace:
        exp = exp.replace(" ", "")
    T: Tuple[RootNode, list] = compile_snippet(exp)
    result, errors = T
    return result


def parse_expression_as(exp, format):
    result = parse_expression(exp)
    return result.serialize(format)


def parse_expression_as_dict(exp: str) -> dict:
    json_str = parse_expression_as(exp, "jsondict")
    tree = json.loads(json_str)
    return tree
