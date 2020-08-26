from __future__ import annotations

import pydantic
import datetime
import asyncio
import typing

from pydantic import BaseModel

from swagger_codegen.api.base import BaseApi
from swagger_codegen.api.request import ApiRequest


class ApiResponse(BaseModel):
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None


def make_request(
    self: BaseApi, __request__: bytes, petid: int, additionalmetadata: str = ...,
) -> ApiResponse:
    """uploads an image"""

    def serialize_item(item):
        if isinstance(item, pydantic.BaseModel):
            return item.dict()
        return item

    if isinstance(__request__, (list, tuple, set)):
        body = [serialize_item(item) for item in __request__]
    else:
        body = __request__.dict()

    m = ApiRequest(
        method="POST",
        path="/api/v3/pet/{petId}/uploadImage".format(petId=petid,),
        content_type="application/json",
        body=body,
        headers=self._only_provided({}),
        query_params=self._only_provided({"additionalMetadata": additionalmetadata,}),
        cookies=self._only_provided({}),
    )
    return self.make_request({"200": {"application/json": ApiResponse,},}, m)
