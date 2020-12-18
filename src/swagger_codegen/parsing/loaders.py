from pathlib import Path
from typing import Optional

from schemathesis import loaders
from schemathesis.schemas import BaseSchema

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
    add_x_names(schema)
    add_x_names_to_plain_response_objects(schema)
    return loaders.from_dict(schema)


def add_x_names(schema):
    """
    Add `x-name` attribute to each schema referenced as $ref.

    This step is needed to provide a name that will be used to render
    request or response data transfer objects for api client's methods.
    """
    for name, schema in schema["components"]["schemas"].items():
        schema["x-name"] = name


def add_x_names_to_plain_response_objects(schema):
    """Add `x-name` attribute to each inlined response object.

    Inlined response object is an object that is defined in `responses`
    section with schema of type `object` instead of `$ref`.

    That is needed to provide a name that will
    be used to render response data transfer object for respective endpoint.
    """
    if "paths" not in schema:
        return

    for uri, path in schema["paths"].items():
        for method_name, method in path.items():
            for status_code, description in method["responses"].items():
                if "content" not in description:
                    continue
                if "application/json" not in description["content"]:
                    continue
                schema = description["content"]["application/json"]["schema"]
                if "type" not in schema:
                    continue
                if schema["type"] != "object":
                    continue
                schema["x-name"] = f"Response{status_code}"
