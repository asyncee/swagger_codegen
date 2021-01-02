from boltons.iterutils import remap
from swagger_codegen.parsing.loaders import (from_file, load_base_schema,
                                             tuple_startswith)


def test_from_file():
    expected = {"test": True, "søk": "search"}
    assert from_file("tests/fixtures/input.json") == expected
    assert from_file("tests/fixtures/input.yaml") == expected


def test_preprocessing():
    for fixture in [
        "tests/fixtures/inline_defined_objects.json",
        "tests/fixtures/minimal_example.json",
    ]:
        schema = load_base_schema(fixture).raw_schema

        def visit(path, key, value):
            if key == "schema" and "type" in value and value["type"] == "object":
                assert "x-name" in value
            return key, value

        remap(schema, visit=visit)


def test_tuple_startswith():
    tpl = (1, 2, "string")
    assert tuple_startswith(tpl)
    assert tuple_startswith(tpl, 1)
    assert tuple_startswith(tpl, 1, 2)
    assert tuple_startswith(tpl, 1, 2, "string")
    assert tuple_startswith(tpl, 1, 2, "string", 3) is False
    assert tuple_startswith(tpl, "x") is False
