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
    petid: int,
    api_key: str = ...,
) -> None:
    """Deletes a pet"""

    body = None

    m = ApiRequest(
        method="DELETE",
        path="/api/v3/pet/{petId}".format(
            petId=petid,
        ),
        content_type=None,
        body=body,
        headers=self._only_provided(
            {
                "api_key": api_key,
            }
        ),
        query_params=self._only_provided({}),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {
            "400": {
                "default": None,
            },
        },
        m,
    )
