from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic.utils import validate_field_name

from .data_type import DataType
from .data_type import ObjectDataType


def make_data_type(schema: dict, parent_types: Optional[List[str]] = None,) -> DataType:
    parent_types = parent_types or []
    c_parent_types = parent_types.copy()

    # Consult with https://pydantic-docs.helpmanual.io/usage/schema/#json-schema-types
    if schema == {}:
        return DataType(python_type="None")

    for field in ("allOf", "anyOf", "oneOf"):
        if field in schema:
            nested_schemas = schema[field]
            members = [make_data_type(n, c_parent_types) for n in nested_schemas]
            if len(members) == 1:
                return DataType(
                    python_type=f"{members[0].python_type}", members=members
                )

            types = [r.python_type for r in members]
            # if len(members) == 2 and "None" in types:
            #     a, b = members
            #     non_null_member = a if b.python_type == "None" else b
            #     return DataType(
            #         python_type=non_null_member.python_type, members=[non_null_member]
            #     )

            nested_types = ", ".join(types)
            return DataType(
                python_type=f"typing.Union[{nested_types}]", members=members
            )

    if "enum" in schema:
        return DataType(python_type="str")

    if "type" not in schema:
        return DataType(python_type="typing.Any")

    if schema["type"] == "string":
        if "format" in schema:
            if schema["format"] == "binary":
                return DataType(python_type="bytes")
            if schema["format"] == "date-time":
                return DataType(python_type="datetime.datetime")
            if schema["format"] == "date":
                return DataType(python_type="datetime.date")
            if schema["format"] == "time":
                return DataType(python_type="time.time")
        return DataType(python_type="str")

    if schema["type"] in ("integer", "number", "boolean", "null"):
        typemap: Dict[str, str] = {
            "boolean": "bool",
            "number": "float",
            "integer": "int",
            "null": "None",
        }
        return DataType(python_type=typemap[schema["type"]])

    if schema["type"] == "object":
        if schema == {"type": "object"}:
            return DataType(python_type="typing.Dict")

        if "additionalProperties" in schema:
            inner_type = make_data_type(schema["additionalProperties"], c_parent_types)
            return DataType(
                python_type=f"typing.Dict[str, {inner_type.python_type}]",
                members=[inner_type],
            )

        if "properties" in schema:
            pt_name = object_name(schema)
            if pt_name in parent_types:
                return ObjectDataType(python_type=pt_name, is_recursive=True)

            c_parent_types.append(pt_name)
            members__ = []

            def member_name_type_value(fname, type, is_required, default):
                value = {
                    "default": repr(default) if default is not None else None,
                    "alias": None,
                }
                name = fname

                try:
                    validate_field_name([BaseModel], fname)
                except NameError:
                    value["alias"] = f'"{name}"'
                    name = f"{fname}_"

                if not is_required and default is None:
                    value["default"] = "None"

                if value["alias"]:
                    return (
                        name,
                        type,
                        "pydantic.Field({default}, alias={alias})".format(**value),
                    )
                return (
                    name,
                    type,
                    value["default"],
                )

            for propname, propschema in schema["properties"].items():
                child_data_type = make_data_type(propschema, c_parent_types)

                name, type, value = member_name_type_value(
                    propname,
                    child_data_type.python_type,
                    propname in schema.get("required", []),
                    default=propschema.get("default"),
                )
                child_data_type.python_type = type
                child_data_type.member_name = name
                child_data_type.member_value = value
                if child_data_type.member_value == "None":
                    child_data_type.is_optional_type = True

                members__.append(child_data_type)

            return ObjectDataType(python_type=pt_name, members=members__)
        return DataType(python_type="typing.Dict")

    if schema["type"] == "array":
        if schema["items"] == {}:
            return DataType(python_type="typing.List")

        inner_type = make_data_type(schema["items"], c_parent_types)
        return DataType(
            python_type=f"typing.List[{inner_type.python_type}]", members=[inner_type]
        )

    raise ValueError(f"Can not get compound type because of invalid schema: {schema}")


def object_name(schema):
    return schema.get("x-name", None)
