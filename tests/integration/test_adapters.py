from typing import Callable

import asyncio
import os
from urllib.parse import urljoin

import aiohttp
import httpx
import pytest
from pydantic import BaseModel

from swagger_codegen.api import json
from swagger_codegen.api.adapter.aiohttp import AiohttpAdapter
from swagger_codegen.api.adapter.base import HttpClientAdapter
from swagger_codegen.api.adapter.httpx import HttpxAdapter
from swagger_codegen.api.adapter.requests import RequestsAdapter
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api.response import ApiResponse


@pytest.fixture
def requests_adapter():
    return RequestsAdapter()


@pytest.yield_fixture
def aiohttp_adapter():
    class AiohttpSyncAdapter(HttpClientAdapter):
        def call(self, api_request: ApiRequest) -> ApiResponse:
            async def _request():
                async with aiohttp.ClientSession() as session:
                    return await AiohttpAdapter(session).call(api_request)

            loop = asyncio.get_event_loop()
            return loop.run_until_complete(loop.create_task(_request()))

    return AiohttpSyncAdapter()


@pytest.yield_fixture
def httpx_adapter():
    class HttpxSyncAdapter(HttpClientAdapter):
        def call(self, api_request: ApiRequest) -> ApiResponse:
            async def _request():
                async with httpx.AsyncClient() as client:
                    return await HttpxAdapter(client).call(api_request)

            loop = asyncio.get_event_loop()
            return loop.run_until_complete(loop.create_task(_request()))

    return HttpxSyncAdapter()


@pytest.fixture(
    params=[
        pytest.lazy_fixture("requests_adapter"),
        pytest.lazy_fixture("aiohttp_adapter"),
        pytest.lazy_fixture("httpx_adapter"),
    ]
)
def adapter(request):
    return request.param


@pytest.fixture
def host():
    return os.getenv("HTTPBIN_HOST", "https://httpbin.org")


@pytest.fixture
def url(host) -> Callable[[str], str]:
    return lambda url_: urljoin(host, url_)


def test_get(url: Callable, adapter: HttpClientAdapter):
    request_url = url("get")
    request = ApiRequest(
        method="GET",
        path=request_url,
        query_params={"value": 10},
        headers={"X-Test-Header": "this-is-test"},
        cookies={"my-cookie": "test"},
    )
    response = adapter.call(request)

    assert isinstance(response, ApiResponse)
    assert isinstance(response.body, dict)

    assert response.body["args"] == {"value": "10"}
    assert response.body["headers"]["X-Test-Header"] == "this-is-test"
    assert response.body["headers"]["Cookie"] == "my-cookie=test"

    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.url == request_url + "?value=10"


@pytest.mark.skip("not implemented")
def test_options(url: Callable, adapter: HttpClientAdapter):
    pass


@pytest.mark.skip("not implemented")
def test_head(url: Callable, adapter: HttpClientAdapter):
    pass


def test_get_image(url: Callable, adapter: HttpClientAdapter):
    request_url = url("image/png")
    request = ApiRequest(
        method="GET",
        path=request_url,
    )
    response = adapter.call(request)

    assert isinstance(response, ApiResponse)
    assert isinstance(response.body, bytes)
    assert response.content_type == "image/png"
    assert response.status_code == 200


def test_post(url: Callable, adapter: HttpClientAdapter):
    class Payload(BaseModel):
        field: str

    request_body = {
        "string": "string",
        "number": 1,
        "list": [1, "string", Payload(field="payload")],
        "bool": True,
    }

    request_url = url("post")
    request = ApiRequest(
        method="POST",
        path=request_url,
        query_params={"value": 10},
        headers={"X-Test-Header": "test"},
        cookies={"my-cookie": "test"},
        content_type="application/json",
        body=request_body,
    )
    response = adapter.call(request)

    assert isinstance(response, ApiResponse)
    assert isinstance(response.body, dict)

    assert response.body["args"] == {"value": "10"}
    assert response.body["headers"]["X-Test-Header"] == "test"
    assert response.body["headers"]["Cookie"] == "my-cookie=test"

    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.url == request_url + "?value=10"
    assert response.body["data"] == json.dumps(request_body)
    assert response.body["json"] == request_body


@pytest.mark.skip("not implemented")
def test_post_form(url: Callable, adapter: HttpClientAdapter):
    # httpbin: /forms/post HTML form that submits to /post
    pass


@pytest.mark.skip("not implemented")
def test_put(url: Callable, adapter: HttpClientAdapter):
    pass


@pytest.mark.skip("not implemented")
def test_delete(url: Callable, adapter: HttpClientAdapter):
    pass


@pytest.mark.skip("not implemented")
def test_patch(url: Callable, adapter: HttpClientAdapter):
    pass
