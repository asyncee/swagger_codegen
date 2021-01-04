from __future__ import annotations

import typing

import datetime

import pydantic
from pydantic import BaseModel

from swagger_codegen.api import json
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


def make_request(
    self: BaseApi,
    username: str,
) -> User:
    """Get user by user name"""

    body = None

    m = ApiRequest(
        method="GET",
        path="/api/v3/user/{username}".format(
            username=username,
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({}),
        query_params=self._only_provided({}),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {
            "200": {
                "application/json": User,
                "application/xml": User,
            },
            "400": {
                "default": None,
            },
            "404": {
                "default": None,
            },
        },
        m,
    )
