from pathlib import Path

from schemathesis import loaders
from schemathesis.schemas import BaseSchema


def _from_json(file: str) -> dict:
    import json

    with open(file) as fd:
        return json.load(fd)


def _from_yaml(file: str):
    import yaml

    with open(file) as fd:
        return yaml.load(fd)


def from_file(file: str):
    parsers = {
        ".json": _from_json,
        ".yaml": _from_yaml,
    }
    return parsers[Path(file).suffix](file)


def from_uri(uri: str) -> dict:
    import requests
    import yaml

    response = requests.get(uri)
    response.raise_for_status()
    return yaml.safe_load(response.text)


def load_base_schema(schema_uri) -> BaseSchema:
    if "://" in schema_uri:
        schema = from_uri(schema_uri)
    else:
        schema = from_file(schema_uri)
    add_x_names(schema)
    return loaders.from_dict(schema)


def add_x_names(schema):
    for name, schema in schema["components"]["schemas"].items():
        schema["x-name"] = name
