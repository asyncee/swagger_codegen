from __future__ import annotations

import datetime
import typing

import pydantic
from pydantic import BaseModel

from swagger_codegen.api import json
from swagger_codegen.api.base import BaseApi
from swagger_codegen.api.request import ApiRequest


def make_request(
    self: BaseApi,
    username: str,
) -> None:
    """Delete user"""

    body = None

    m = ApiRequest(
        method="DELETE",
        path="/api/v3/user/{username}".format(
            username=username,
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
