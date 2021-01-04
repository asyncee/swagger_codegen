from __future__ import annotations

import typing

import datetime

import pydantic
from pydantic import BaseModel

from swagger_codegen.api import json
from swagger_codegen.api.base import BaseApi
from swagger_codegen.api.request import ApiRequest


def make_request(
    self: BaseApi,
) -> typing.Dict[str, int]:
    """Returns pet inventories by status"""

    body = None

    m = ApiRequest(
        method="GET",
        path="/api/v3/store/inventory".format(),
        content_type=None,
        body=body,
        headers=self._only_provided({}),
        query_params=self._only_provided({}),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {
            "200": {
                "application/json": typing.Dict[str, int],
            },
        },
        m,
    )
