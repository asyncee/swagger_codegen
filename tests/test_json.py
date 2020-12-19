import datetime as dt
import uuid

from pydantic import BaseModel
from swagger_codegen.api import json


class TestPydanticClass(BaseModel):
    field: str


def test_json_dumps():
    now = dt.datetime(2020, 1, 1)
    uuid_ = uuid.UUID(int=0x12345678123456781234567812345678)

    expected = """
{
  "string": "string",
  "number": 1,
  "date": "2020-01-01",
  "datetime": "2020-01-01T00:00:00",
  "list": [
    1,
    2,
    3
  ],
  "tuple": [
    1,
    2,
    3
  ],
  "set": [
    1,
    2,
    3
  ],
  "complex_list": [
    {
      "field": "one"
    },
    1,
    2,
    3,
    "12345678-1234-5678-1234-567812345678"
  ]
}
""".strip()

    assert (
        json.dumps(
            {
                "string": "string",
                "number": 1,
                "date": now.date(),
                "datetime": now,
                "list": [1, 2, 3],
                "tuple": [1, 2, 3],
                "set": [1, 2, 3],
                "complex_list": [
                    TestPydanticClass(field="one"),
                    1,
                    2,
                    3,
                    uuid_,
                ],
            },
            indent=2,
        )
        == expected
    )
