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
    username: str = ...,
    password: str = ...,
) -> str:
    """Logs user into the system"""

    body = None

    m = ApiRequest(
        method="GET",
        path="/api/v3/user/login".format(),
        content_type=None,
        body=body,
        headers=self._only_provided({}),
        query_params=self._only_provided(
            {
                "username": username,
                "password": password,
            }
        ),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {
            "200": {
                "application/json": str,
                "application/xml": str,
            },
            "400": {
                "default": None,
            },
        },
        m,
    )
