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


def make_request(self, status: str = "available",) -> typing.List[Pet]:
    """Finds Pets by status"""
    m = ApiRequest(
        method="GET",
        path="/api/v3/pet/findByStatus".format(),
        content_type=None,
        body=None,
        headers=self._only_provided({}),
        query_params=self._only_provided({"status": status,}),
        cookies=self._only_provided({}),
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
