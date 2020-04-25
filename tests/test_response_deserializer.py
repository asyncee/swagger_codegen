import typing

import pytest
from pydantic import BaseModel

from swagger_codegen.api.response_deserializer import DefaultResponseDeserializer
from swagger_codegen.api.response_deserializer import ResponseDeserializer


class PydanticClass(BaseModel):
    field: str


@pytest.fixture
def d() -> ResponseDeserializer:
    return DefaultResponseDeserializer()


def test_default_response_deserializer(d: ResponseDeserializer):
    assert d.deserialize(None, None) is None
    assert d.deserialize(str, None) is None
    assert d.deserialize(None, {}) is None

    assert d.deserialize(typing.List[dict], [{"a dict": True}]) == [{"a dict": True}]
    assert d.deserialize(typing.List[str], ["one", "two"]) == ["one", "two"]
    assert d.deserialize(typing.List[PydanticClass], [{"field": "value"}]) == [
        PydanticClass(field="value")
    ]

    assert d.deserialize(typing.Set[str], ["one", "two"]) == {"one", "two"}

    assert d.deserialize(typing.Dict, {"a dict": True}) == {"a dict": True}
    assert d.deserialize(typing.Dict[str, int], {"value": 200}) == {"value": 200}
    assert d.deserialize(typing.Dict[str, int], {"value": "201"}) == {"value": 201}

    assert d.deserialize(PydanticClass, {"field": "hello"}) == PydanticClass(
        field="hello"
    )

    assert d.deserialize(str, "a string") == "a string"
    assert d.deserialize(list, [1, 2, 3]) == [1, 2, 3]
    assert d.deserialize(set, {1, 2, 3}) == {1, 2, 3}
