import string
from itertools import dropwhile

import inflection

allowed_chars = string.ascii_letters + string.digits + "_"


def start_with_valid_characters(name: str) -> str:
    return "".join(
        [c for c in dropwhile(lambda s: s not in string.ascii_letters + "_", name)]
    )


def replace_chars(name: str) -> str:
    return name.replace("-", "_").replace(" ", "_")


def strip_chars(name: str) -> str:
    return "".join([c for c in name if c in allowed_chars])


def to_classname(name: str) -> str:
    name = start_with_valid_characters(name)
    name = inflection.camelize(replace_chars(name))
    return strip_chars(name)


def to_identifier(name: str) -> str:
    name = start_with_valid_characters(name)
    name = inflection.underscore(replace_chars(name))
    return strip_chars(name)


def test_to_classname():
    cases = {
        "A B": "AB",
        "The Word": "TheWord",
        "TestCase": "TestCase",
        "Test-Case": "TestCase",
        "Test.Case": "TestCase",
        "[TestCase]": "TestCase",
        "theTestCase1": "TheTestCase1",
        "1234identifier": "Identifier",
    }
    for case, expected in cases.items():
        assert to_classname(case) == expected


def test_to_identifier():
    cases = {
        "A B": "a_b",
        "The Word": "the_word",
        "TestCase": "test_case",
        "Test-Case": "test_case",
        "Test.Case": "testcase",
        "[TestCase]": "test_case",
        "theTestCase1": "the_test_case1",
        "1234identifier": "identifier",
    }
    for case, expected in cases.items():
        assert to_identifier(case) == expected