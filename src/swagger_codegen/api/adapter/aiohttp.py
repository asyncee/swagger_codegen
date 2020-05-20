from functools import partial

import aiohttp
from aiohttp import ContentTypeError

from swagger_codegen.api.adapter.base import HttpClientAdapter
from swagger_codegen.api.adapter.params_converter import AiohttpParamsConverter
from swagger_codegen.api.adapter.params_converter import ParamsConverter
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api.response import ApiResponse
from swagger_codegen.api.types import APPLICATION_JSON


class AiohttpAdapter(HttpClientAdapter):
    def __init__(
        self,
        session: aiohttp.ClientSession,
        params_converter: ParamsConverter = AiohttpParamsConverter(),
    ):
        self._session = session
        self._params_converter = params_converter

    def call(self, api_request: ApiRequest) -> ApiResponse:
        methods = {
            "get": partial(self._read, self._session.get),
            "options": partial(self._read, self._session.options),
            "head": partial(self._read, self._session.head),
            "put": partial(self._write, self._session.put),
            "delete": partial(self._write, self._session.delete),
            "patch": partial(self._write, self._session.patch),
            "post": partial(self._write, self._session.post),
        }
        return methods[api_request.method](api_request=api_request)

    async def _read(self, make_request, api_request: ApiRequest):
        async with make_request(
            url=api_request.path,
            params=self._params_converter.convert_query_params(
                api_request.query_params
            ),
            headers=api_request.headers,
            cookies=api_request.cookies,
        ) as response:
            return await self._make_response(response)

    async def _write(self, make_request, api_request: ApiRequest):
        params = dict(
            url=api_request.path,
            params=self._params_converter.convert_query_params(
                api_request.query_params
            ),
            headers=api_request.headers,
            cookies=api_request.cookies,
        )

        if (
            api_request.body is not None
            and api_request.content_type == APPLICATION_JSON
        ):
            params["json"] = api_request.body
        else:
            params["data"] = api_request.body

        async with make_request(**params) as response:
            return await self._make_response(response)

    async def _make_response(self, response: aiohttp.ClientResponse) -> ApiResponse:
        try:
            body = await response.json()
        except ContentTypeError:
            body = await response.read()

        return ApiResponse(
            url=str(response.url),
            body=body,
            headers=dict(response.headers),
            status_code=int(response.status),
            content_type=response.content_type,
        )
