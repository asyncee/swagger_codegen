import string
from itertools import dropwhile

import inflection

allowed_chars = string.ascii_letters + string.digits + "_"


def start_with_valid_characters(name: str) -> str:
    return "".join(
        c for c in dropwhile(lambda s: s not in string.ascii_letters + "_", name)
    )


def replace_chars(name: str) -> str:
    return name.replace("-", "_").replace(" ", "_")


def strip_chars(name: str) -> str:
    return "".join(c for c in name if c in allowed_chars)


def to_classname(name: str) -> str:
    name = start_with_valid_characters(name)
    name = inflection.camelize(replace_chars(name))
    return strip_chars(name)


def to_identifier(name: str) -> str:
    name = start_with_valid_characters(name)
    name = inflection.underscore(replace_chars(name))
    return strip_chars(name)
