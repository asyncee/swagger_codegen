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
) -> None:
    """Logs out current logged in user session"""

    body = None

    m = ApiRequest(
        method="GET",
        path="/api/v3/user/logout".format(),
        content_type=None,
        body=body,
        headers=self._only_provided({}),
        query_params=self._only_provided({}),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {
            "default": {
                "default": None,
            },
        },
        m,
    )
