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


def make_request(self, __request__: Pet,) -> Pet:
    """Add a new pet to the store"""
    m = ApiRequest(
        method="POST",
        path="/api/v3/pet".format(),
        content_type="application/json",
        body=__request__.dict(),
        headers=self._only_provided({}, exclude_none=True),
        query_params=self._only_provided({}, exclude_none=True),
        cookies=self._only_provided({}, exclude_none=True),
    )
    return self.make_request(
        {"200": {"application/json": Pet, "application/xml": Pet,},}, m
    )
