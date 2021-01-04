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
    name: str = ...,
    status: str = ...,
) -> None:
    """Updates a pet in the store with form data"""

    body = None

    m = ApiRequest(
        method="POST",
        path="/api/v3/pet/{petId}".format(
            petId=petid,
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({}),
        query_params=self._only_provided(
            {
                "name": name,
                "status": status,
            }
        ),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {
            "405": {
                "default": None,
            },
        },
        m,
    )
