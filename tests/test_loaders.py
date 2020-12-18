from swagger_codegen.parsing.loaders import from_file


def test_from_file():
    expected = {"test": True, "søk": "search"}
    assert from_file("tests/fixtures/input.json") == expected
    assert from_file("tests/fixtures/input.yaml") == expected
