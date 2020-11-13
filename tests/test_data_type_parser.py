import pytest
from swagger_codegen.parsing.data_type import DataType, ObjectDataType
from swagger_codegen.parsing.data_type_parser import make_data_type


def test_parse_empty_schema():
    data_type = make_data_type({})
    assert data_type == DataType(python_type="None")


def test_parse_all_of_any_of_one_of():
    int_schema = {"type": "integer"}
    object_schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "required": ["name"],
    }

    fields = ("oneOf", "allOf", "anyOf")

    for field in fields:
        data_type = make_data_type({field: [int_schema]})
        assert data_type == DataType(
            python_type="int", members=[DataType(python_type="int")]
        )

        data_type = make_data_type({field: [int_schema, {}]})
        assert data_type == DataType(
            python_type="typing.Union[int, None]",
            members=[DataType(python_type="int"), DataType(python_type="None")],
        )

        data_type = make_data_type({field: [object_schema]})
        assert data_type == DataType(
            python_type="None",
            members=[
                ObjectDataType(
                    python_type=None,
                    members=[
                        DataType(
                            python_type="str",
                            member_name="name",
                        )
                    ],
                )
            ],
        )


def test_parse_enum():
    data_type = make_data_type({"enum": ["one", "two"]})
    assert data_type == DataType(python_type="str")

    data_type = make_data_type({"title": "PriceType", "enum": [1], "type": "integer"})
    assert data_type == DataType(python_type="int")


def test_parse_missing_schema():
    data_type = make_data_type({"description": "string"})
    assert data_type == DataType(python_type="typing.Any")


def test_parse_string():
    assert make_data_type({"type": "string", "format": "binary"}) == DataType(
        python_type="bytes"
    )
    assert make_data_type({"type": "string", "format": "date-time"}) == DataType(
        python_type="datetime.datetime"
    )
    assert make_data_type({"type": "string", "format": "date"}) == DataType(
        python_type="datetime.date"
    )
    assert make_data_type({"type": "string", "format": "time"}) == DataType(
        python_type="time.time"
    )
    assert make_data_type({"type": "string"}) == DataType(python_type="str")


def test_parse_primitive_types():
    assert make_data_type({"type": "integer"}) == DataType(python_type="int")
    assert make_data_type({"type": "number"}) == DataType(python_type="float")
    assert make_data_type({"type": "boolean"}) == DataType(python_type="bool")
    assert make_data_type({"type": "null"}) == DataType(python_type="None")


def test_parse_array():
    assert make_data_type({"type": "array", "items": {}}) == DataType(
        python_type="typing.List"
    )
    assert make_data_type({"type": "array", "items": {"type": "integer"}}) == DataType(
        python_type="typing.List[int]", members=[DataType(python_type="int")]
    )


def test_parse_object():
    assert make_data_type({"type": "object"}) == DataType(python_type="typing.Dict")

    assert make_data_type(
        {"type": "object", "additionalProperties": {"type": "boolean"}}
    ) == DataType(
        python_type="typing.Dict[str, bool]", members=[DataType(python_type="bool")]
    )


def test_parse_complex_object():
    assert make_data_type(
        {
            "x-name": "Obj1",
            "type": "object",
            "properties": {
                "field1": {"type": "integer"},
                "field2": {"type": "string", "default": "some-value"},
            },
        }
    ) == ObjectDataType(
        python_type="Obj1",
        members=[
            DataType(
                python_type="int",
                member_name="field1",
                member_value="None",
                is_optional_type=True,
            ),
            DataType(
                python_type="str", member_name="field2", member_value="'some-value'"
            ),
        ],
    )


def test_parse_object_with_alias_field():
    assert make_data_type(
        {
            "x-name": "Obj",
            "type": "object",
            "properties": {"fields": {"type": "string", "default": "yes"}},
        }
    ) == ObjectDataType(
        python_type="Obj",
        members=[
            DataType(
                python_type="str",
                member_name="fields_",
                member_value="pydantic.Field('yes', alias=\"fields\")",
            ),
        ],
    )

    assert make_data_type(
        {
            "x-name": "Obj",
            "type": "object",
            "properties": {"fields": {"type": "integer"}},
        }
    ) == ObjectDataType(
        python_type="Obj",
        members=[
            DataType(
                python_type="int",
                member_name="fields_",
                member_value='pydantic.Field(None, alias="fields")',
            ),
        ],
    )


def test_parse_object_with_required_and_or_default():
    r = make_data_type(
        {
            "x-name": "Obj",
            "type": "object",
            "properties": {
                "a": {"type": "string", "default": "a"},
                "b": {"type": "string", "default": "b"},
                "c": {"type": "string"},
                "d": {"type": "string"},
            },
            "required": ["a", "c"],
        }
    )
    assert r == ObjectDataType(
        python_type="Obj",
        members=[
            DataType(
                python_type="str",
                member_name="a",
                member_value="'a'",
            ),
            DataType(python_type="str", member_name="b", member_value="'b'"),
            DataType(python_type="str", member_name="c"),
            DataType(
                python_type="str",
                member_name="d",
                member_value="None",
                is_optional_type=True,
            ),
        ],
    )


def test_parse_object_with_recursive_reference():
    assert make_data_type(
        {
            "x-name": "Obj1",
            "type": "object",
            "required": ["recursive"],
            "properties": {
                "recursive": {
                    "x-name": "Obj1",
                    "type": "object",
                    "required": ["recursive"],
                    "properties": {
                        "recursive": {
                            "x-name": "Obj1",
                            "type": "object",
                            "properties": {"recursive": {}},
                            "required": ["recursive"],
                        },
                    },
                },
            },
        }
    ) == ObjectDataType(
        python_type="Obj1",
        members=[
            ObjectDataType(
                python_type="Obj1",
                member_name="recursive",
                is_recursive=True,
            ),
        ],
    )


def test_parse_raises_if_schema_is_invalid():
    with pytest.raises(ValueError):
        make_data_type({"something": True, "type": "invalid"})


def test_parse_nested_object():
    data_type = make_data_type(
        {
            "x-name": "top_level_model",
            "type": "object",
            "properties": {
                "string_property": {"type": "string"},
                "nested_property": {
                    "type": "object",
                    "properties": {
                        "number_property": {
                            "type": "number",
                        },
                    },
                },
            },
        },
    )
    assert data_type == ObjectDataType(
        python_type="top_level_model",
        members=[
            DataType(
                python_type="str",
                member_name="string_property",
                member_value="None",
                is_optional_type=True,
                is_recursive=False,
            ),
            ObjectDataType(
                python_type="top_level_modelNested_property",
                member_name="nested_property",
                member_value="None",
                is_optional_type=True,
                is_recursive=False,
                members=[
                    DataType(
                        python_type="float",
                        member_name="number_property",
                        is_optional_type=True,
                        member_value="None",
                    )
                ],
            ),
        ],
    )
