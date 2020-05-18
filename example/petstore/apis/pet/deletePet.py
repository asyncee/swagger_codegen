from __future__ import annotations

import pydantic
import datetime
import asyncio
import typing

from pydantic import BaseModel

from swagger_codegen.api.request import ApiRequest


def make_request(self, petid: int, api_key: str = ...,) -> None:
    """Deletes a pet"""
    m = ApiRequest(
        method="DELETE",
        path="/api/v3/pet/{petId}".format(petId=petid,),
        content_type=None,
        body=None,
        headers=self._only_provided({"api_key": api_key,}, exclude_none=True),
        query_params=self._only_provided({}, exclude_none=True),
        cookies=self._only_provided({}, exclude_none=True),
    )
    return self.make_request({}, m)
