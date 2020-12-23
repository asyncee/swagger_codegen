import datetime as dt

import pytest
from multidict import MultiDict

from swagger_codegen.api.adapter.params_converter import (
    AiohttpParamsConverter,
    DefaultParamsConverter,
)


@pytest.fixture()
def params():
    return {
        "a": 1,
        "datetime": dt.datetime(2020, 1, 1, 12, 0, 5),
        "list": [1, 2, 3],
        "tuple": [3, 4, 5],
        "none": None,
    }


def test_default_params_converter(params):
    converter = DefaultParamsConverter()
    expected = {
        "a": 1,
        "datetime": "2020-01-01T12:00:05",
        "list": [1, 2, 3],
        "tuple": [3, 4, 5],
    }
    result = converter.convert_query_params(params)
    assert isinstance(result, dict)
    assert result == expected


def test_aiohttp_default_params_converter(params):
    converter = AiohttpParamsConverter()
    expected = MultiDict(
        {
            "a": 1,
            "datetime": "2020-01-01T12:00:05",
        }
    )
    expected.add("list", 1)
    expected.add("list", 2)
    expected.add("list", 3)
    expected.add("tuple", 3)
    expected.add("tuple", 4)
    expected.add("tuple", 5)

    result = converter.convert_query_params(params)
    assert isinstance(result, MultiDict)
    assert result == expected
