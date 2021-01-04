from typing import Dict, List, Optional

from pydantic import BaseModel
from pydantic.utils import validate_field_name

from ..render.utils import to_classname
from .data_type import DataType, ObjectDataType

Schema = dict
ParentTypes = List[str]


def handle_all_any_one_of(
    schema: Schema,
    parent_schema: Optional[Schema],
    parent_types: Optional[ParentTypes],
    for_writes: bool,
) -> Optional[DataType]:
    for field in ("allOf", "anyOf", "oneOf"):
        if field in schema:
            nested_schemas = schema[field]
            members = [
                make_data_type(
                    member_def,
                    parent_types,
                    parent_schema=schema,
                    for_writes=for_writes,
                )
                for member_def in nested_schemas
            ]

            if parent_schema:
                member_property_name = None

                if "properties" in parent_schema:
                    for property_field_name, property_schema in parent_schema["properties"].items():
                        if property_schema is schema:
                            member_property_name = property_field_name
                            break

                if member_property_name:
                    for i, member in enumerate(members):
                        if member.python_type is None:
                            member.python_type = to_classname(f"{member_property_name}{i + 1}")

            if len(members) == 1:
                return DataType(python_type=f"{members[0].python_type}", members=members)

            types = [r.python_type for r in members]

            nested_types = ", ".join(types)
            return DataType(python_type=f"typing.Union[{nested_types}]", members=members)
    return None


def handle_enum(schema: Schema, for_writes: bool) -> DataType:
    if "type" in schema:
        del schema["enum"]
        return make_data_type(schema, for_writes=for_writes)
    return DataType(python_type="str")


def handle_string(schema: Schema) -> DataType:
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


def handle_primitives(schema: Schema) -> DataType:
    typemap: Dict[str, str] = {
        "boolean": "bool",
        "number": "float",
        "integer": "int",
        "null": "None",
    }
    return DataType(python_type=typemap[schema["type"]])


def handle_array(schema: Schema, parent_types: Optional[ParentTypes], for_writes: bool) -> DataType:
    if schema["items"] == {}:
        return DataType(python_type="typing.List")

    inner_type = make_data_type(
        schema["items"],
        parent_types,
        parent_schema=schema,
        for_writes=for_writes,
    )
    return DataType(python_type=f"typing.List[{inner_type.python_type}]", members=[inner_type])


def handle_object_dict(schema: Schema, parent_types: Optional[ParentTypes], for_writes: bool):
    if isinstance(schema["additionalProperties"], bool) or not schema["additionalProperties"]:
        return DataType(python_type="typing.Dict")

    inner_type = make_data_type(
        schema["additionalProperties"],
        parent_types,
        parent_schema=schema,
        for_writes=for_writes,
    )
    return DataType(
        python_type=f"typing.Dict[str, {inner_type.python_type}]",
        members=[inner_type],
    )


def prepare_pydantic_field(field_name, type, is_required, default):
    value = {
        "default": repr(default) if default is not None else None,
        "alias": None,
    }
    try:
        validate_field_name([BaseModel], field_name)
    except NameError:
        value["alias"] = f'"{field_name}"'
        maybe_aliased_name = f"{field_name}_"
    else:
        maybe_aliased_name = field_name

    if not is_required and default is None:
        value["default"] = "None"

    if value["alias"]:
        return (
            maybe_aliased_name,
            type,
            "pydantic.Field({default}, alias={alias})".format(**value),
        )
    return (
        maybe_aliased_name,
        type,
        value["default"],
    )


def handle_object(
    schema: Schema,
    parent_schema: Optional[Schema],
    parent_types: Optional[ParentTypes],
    for_writes: bool,
) -> DataType:
    parent_types_copy = parent_types.copy()

    if schema == {"type": "object"}:
        return DataType(python_type="typing.Dict")

    if "additionalProperties" in schema:
        return handle_object_dict(schema, parent_types, for_writes)

    if "properties" not in schema:
        return DataType(python_type="typing.Dict")

    parent_type_name = object_name(schema)

    # Case when parent has a field that is an object that does not have a name.
    # In that situation such field must be rendered as a separate python model (class)
    # with name of <parent_type_name><field_name>
    if parent_type_name is None and parent_schema and "properties" in parent_schema:
        parent_props = parent_schema["properties"].items()
        for parent_property_name, parent_property_schema in parent_props:
            if parent_property_schema is schema:
                parent_name_part = "_".join([p for p in parent_types if p is not None])
                parent_type_name = (
                    f"{parent_name_part}{parent_property_name[0].upper()}{parent_property_name[1:]}"
                )
                break

    if parent_type_name in parent_types:
        return ObjectDataType(python_type=parent_type_name, is_recursive=True)

    parent_types_copy.append(parent_type_name)
    object_members = []

    for property_name, property_schema in schema["properties"].items():
        if for_writes and property_schema.get("readOnly"):
            # We don't want to expose read-only properties when we want to write.
            continue

        child_data_type = make_data_type(
            property_schema,
            parent_types_copy,
            parent_schema=schema,
            for_writes=for_writes,
        )

        field_name, field_type, field_value = prepare_pydantic_field(
            property_name,
            child_data_type.python_type,
            property_name in schema.get("required", []),
            default=property_schema.get("default"),
        )
        child_data_type.member_name = field_name
        child_data_type.python_type = field_type
        child_data_type.member_value = field_value
        if field_value == "None":
            child_data_type.is_optional_type = True

        object_members.append(child_data_type)

    return ObjectDataType(python_type=parent_type_name, members=object_members)


def make_data_type(
    schema: Schema,
    parent_types: Optional[ParentTypes] = None,
    parent_schema: Optional[Schema] = None,
    for_writes: bool = False,
) -> DataType:
    parent_types = parent_types or []

    # Consult with https://pydantic-docs.helpmanual.io/usage/schema/#json-schema-types
    if schema == {}:
        return DataType(python_type="None")

    if typ := handle_all_any_one_of(schema, parent_schema, parent_types, for_writes):
        return typ

    if "enum" in schema:
        return handle_enum(schema, for_writes)

    if "type" not in schema:
        return DataType(python_type="typing.Any")

    if schema["type"] == "string":
        return handle_string(schema)

    if schema["type"] in ("integer", "number", "boolean", "null"):
        return handle_primitives(schema)

    if schema["type"] == "object":
        return handle_object(schema, parent_schema, parent_types, for_writes)

    if schema["type"] == "array":
        return handle_array(schema, parent_types, for_writes)

    raise ValueError(f"Can not get compound type because of invalid schema: {schema}")


def object_name(schema):
    return schema.get("x-name", None)
