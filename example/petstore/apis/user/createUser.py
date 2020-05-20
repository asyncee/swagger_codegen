from __future__ import annotations

import pydantic
import datetime
import asyncio
import typing

from pydantic import BaseModel

from swagger_codegen.api.request import ApiRequest


class User(BaseModel):
    email: typing.Optional[str] = None
    firstName: typing.Optional[str] = None
    id: typing.Optional[int] = None
    lastName: typing.Optional[str] = None
    password: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    username: typing.Optional[str] = None
    userStatus: typing.Optional[int] = None


def make_request(self, __request__: User,) -> None:
    """Create user"""
    m = ApiRequest(
        method="POST",
        path="/api/v3/user".format(),
        content_type="application/json",
        body=__request__.dict(),
        headers=self._only_provided({}),
        query_params=self._only_provided({}),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {"default": {"application/json": User, "application/xml": User,},}, m
    )
