from __future__ import annotations

import pydantic
import datetime
import asyncio
import typing

from pydantic import BaseModel

from swagger_codegen.api.request import ApiRequest


class Tag(BaseModel):
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None


class Category(BaseModel):
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None


class Pet(BaseModel):
    id: typing.Optional[int] = None
    name: str
    category: typing.Optional[Category] = None
    photoUrls: typing.List[str]
    tags: typing.Optional[typing.List[Tag]] = None
    status: typing.Optional[str] = None


def make_request(self, tags: typing.List[str] = ...,) -> typing.List[Pet]:
    """Finds Pets by tags"""
    m = ApiRequest(
        method="GET",
        path="/api/v3/pet/findByTags".format(),
        content_type=None,
        body=None,
        headers=self._only_provided({}, exclude_none=True),
        query_params=self._only_provided({"tags": tags,}, exclude_none=True),
        cookies=self._only_provided({}, exclude_none=True),
    )
    return self.make_request(
        {
            "200": {
                "application/json": typing.List[Pet],
                "application/xml": typing.List[Pet],
            },
        },
        m,
    )
