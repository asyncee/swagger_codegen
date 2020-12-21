from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from swagger_codegen.api.base import BaseApi
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api import json


class ApiResponse(BaseModel):
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None


def make_request(
    self: BaseApi,
    __request__: bytes,
    petid: int,
    additionalmetadata: str = ...,
) -> ApiResponse:
    """uploads an image"""

    body = __request__

    m = ApiRequest(
        method="POST",
        path="/api/v3/pet/{petId}/uploadImage".format(
            petId=petid,
        ),
        content_type="application/json",
        body=body,
        headers=self._only_provided({}),
        query_params=self._only_provided(
            {
                "additionalMetadata": additionalmetadata,
            }
        ),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {
            "200": {
                "application/json": ApiResponse,
            },
        },
        m,
    )
