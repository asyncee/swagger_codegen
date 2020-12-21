from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from swagger_codegen.api.base import BaseApi
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api import json


def make_request(
    self: BaseApi,
    orderid: int,
) -> None:
    """Delete purchase order by ID"""

    body = None

    m = ApiRequest(
        method="DELETE",
        path="/api/v3/store/order/{orderId}".format(
            orderId=orderid,
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({}),
        query_params=self._only_provided({}),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {
            "400": {
                "default": None,
            },
            "404": {
                "default": None,
            },
        },
        m,
    )
