from .utils import to_classname, to_identifier


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
