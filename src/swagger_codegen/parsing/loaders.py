from typing import Optional

from copy import deepcopy
from pathlib import Path

from boltons.iterutils import remap
from schemathesis import loaders
from schemathesis.schemas import BaseSchema

from swagger_codegen.render.utils import has_invalid_characters, to_classname

DEFAULT_ENCODING = "utf-8"


def _from_json(file: str, encoding: Optional[str] = None) -> dict:
    import json

    with open(
        file,
        encoding=encoding,
    ) as fd:
        return json.load(fd)


def _from_yaml(file: str, encoding: Optional[str] = None):
    import yaml

    with open(file, encoding=encoding) as fd:
        return yaml.safe_load(fd)


def from_file(file: str, encoding: Optional[str] = None):
    parsers = {
        ".json": _from_json,
        ".yaml": _from_yaml,
    }
    return parsers[Path(file).suffix](file, encoding)


def from_uri(uri: str) -> dict:
    import requests
    import yaml

    response = requests.get(uri)
    response.raise_for_status()
    return yaml.safe_load(response.text)


def load_base_schema(schema_uri, encoding: Optional[str] = None) -> BaseSchema:
    if "://" in schema_uri:
        schema = from_uri(schema_uri)
    else:
        schema = from_file(schema_uri, encoding=encoding or DEFAULT_ENCODING)
    schema = add_component_names(schema)
    schema = add_request_response_names(schema)
    return loaders.from_dict(schema)


def add_component_names(schema: dict):
    """
    Add `x-name` attribute to each schema referenced as $ref.

    This step is needed to provide a name that will be used to render
    request or response data transfer objects for api client's methods.
    """
    if "components" not in schema:
        return schema

    schema = deepcopy(schema)

    for name, inner_schema in schema["components"]["schemas"].items():
        if has_invalid_characters(name):
            name = to_classname(name)
        inner_schema["x-name"] = name

    return schema


def add_request_response_names(schema: dict):
    """Add `x-name` attribute to each inlined response object.

    Inlined response object is an object that is defined in `responses`
    section with schema of type `object` instead of `$ref`.

    That is needed to provide a name that will
    be used to render response data transfer object for respective endpoint.
    """

    def visit(path, key, value):
        def handle_path(path_, value_):
            if tuple_startswith(path_, "paths") and "requestBody" in path_:
                url = path_[1]
                method_name = path_[2]
                value_["x-name"] = to_classname(f"{url}{method_name}Request")
            if tuple_startswith(path_, "paths") and "responses" in path_:
                status_code = path_[4]
                value_["x-name"] = f"Response{status_code}"
            if tuple_startswith(path_, "components", "requestBodies"):
                request_body_name = path_[2]
                value_["x-name"] = request_body_name
            return value_

        if key == "schema" and "type" in value:
            if value["type"] == "object" and "x-name" not in value:
                value = handle_path(path, value)
            elif value["type"] == "array":
                value["items"] = handle_path(path, value["items"])
        return key, value

    return remap(schema, visit=visit)


def tuple_startswith(tpl, *items):
    if len(tpl) < len(items):
        return False
    return tpl[: len(items)] == items
