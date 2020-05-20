from __future__ import annotations

import pydantic
import datetime
import asyncio
import typing

from pydantic import BaseModel

from swagger_codegen.api.request import ApiRequest


def make_request(self, petid: int, name: str = ..., status: str = ...,) -> None:
    """Updates a pet in the store with form data"""
    m = ApiRequest(
        method="POST",
        path="/api/v3/pet/{petId}".format(petId=petid,),
        content_type=None,
        body=None,
        headers=self._only_provided({}),
        query_params=self._only_provided({"name": name, "status": status,}),
        cookies=self._only_provided({}),
    )
    return self.make_request({}, m)
