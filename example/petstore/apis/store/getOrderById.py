from __future__ import annotations

import pydantic
import datetime
import asyncio
import typing

from pydantic import BaseModel

from swagger_codegen.api.base import BaseApi
from swagger_codegen.api.request import ApiRequest


class Order(BaseModel):
    complete: typing.Optional[bool] = None
    id: typing.Optional[int] = None
    petId: typing.Optional[int] = None
    quantity: typing.Optional[int] = None
    shipDate: typing.Optional[datetime.datetime] = None
    status: typing.Optional[str] = None


def make_request(self: BaseApi, orderid: int,) -> Order:
    """Find purchase order by ID"""
    m = ApiRequest(
        method="GET",
        path="/api/v3/store/order/{orderId}".format(orderId=orderid,),
        content_type=None,
        body=None,
        headers=self._only_provided({}),
        query_params=self._only_provided({}),
        cookies=self._only_provided({}),
    )
    return self.make_request(
        {
            "200": {"application/json": Order, "application/xml": Order,},
            "400": {"default": None,},
            "404": {"default": None,},
        },
        m,
    )
