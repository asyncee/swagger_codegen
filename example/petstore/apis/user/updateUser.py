from __future__ import annotations

import pydantic
import datetime
import asyncio
import typing

from pydantic import BaseModel

from swagger_codegen.api.base import BaseApi
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


def make_request(self: BaseApi, __request__: User, username: str,) -> None:
    """Update user"""

    def serialize_item(item):
        if isinstance(item, pydantic.BaseModel):
            return item.dict()
        return item

    if isinstance(__request__, (list, tuple, set)):
        body = [serialize_item(item) for item in __request__]
    else:
        body = __request__.dict()

    m = ApiRequest(
        method="PUT",
        path="/api/v3/user/{username}".format(username=username,),
        content_type="application/json",
        body=body,
        headers=self._only_provided({}),
        query_params=self._only_provided({}),
        cookies=self._only_provided({}),
    )
    return self.make_request({"default": {"default": None,},}, m)
