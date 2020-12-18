import datetime
import json
import typing

import pytest
from pydantic import BaseModel

from swagger_codegen.api.response_deserializer import (
    DefaultResponseDeserializer, ResponseDeserializer)


class PydanticClass(BaseModel):
    field: str
    date: datetime.date


@pytest.fixture
def d() -> ResponseDeserializer:
    return DefaultResponseDeserializer()


def test_default_response_deserializer(d: ResponseDeserializer):
    date = datetime.date(2020, 12, 1)
    assert d.deserialize(None, None) is None
    assert d.deserialize(str, None) is None
    assert d.deserialize(None, {}) is None

    assert d.deserialize(typing.List[dict], [{"a dict": True}]) == [{"a dict": True}]
    assert d.deserialize(typing.List[str], ["one", "two"]) == ["one", "two"]
    assert d.deserialize(
        typing.List[PydanticClass], [{"field": "value", "date": date}]
    ) == [PydanticClass(field="value", date=date)]

    assert d.deserialize(typing.Set[str], ["one", "two"]) == {"one", "two"}

    assert d.deserialize(typing.Dict, {"a dict": True}) == {"a dict": True}
    assert d.deserialize(typing.Dict[str, int], {"value": 200}) == {"value": 200}
    assert d.deserialize(typing.Dict[str, int], {"value": "201"}) == {"value": 201}

    assert d.deserialize(
        PydanticClass, {"field": "hello", "date": date}
    ) == PydanticClass(
        field="hello",
        date=date,
    )

    assert d.deserialize(str, "a string") == "a string"
    assert d.deserialize(list, [1, 2, 3]) == [1, 2, 3]
    assert d.deserialize(set, {1, 2, 3}) == {1, 2, 3}


def test_pydantic_serializer():
    date = datetime.date(2020, 12, 1)
    resource = PydanticClass(field="hello", date=date)
    assert resource.dict() == {"field": "hello", "date": date}
    assert resource.json() == json.dumps({"field": "hello", "date": "2020-12-01"})
    with pytest.raises(TypeError) as execinfo:
        json.dumps(resource.dict())
    assert str(execinfo.value) == "Object of type date is not JSON serializable"
