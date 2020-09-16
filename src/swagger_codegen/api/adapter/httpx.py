from functools import partial

import httpx
from swagger_codegen.api.adapter.base import HttpClientAdapter
from swagger_codegen.api.adapter.params_converter import (
    DefaultParamsConverter,
    ParamsConverter,
)
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api.response import ApiResponse
from swagger_codegen.api.types import APPLICATION_JSON


class HttpxAdapter(HttpClientAdapter):
    def __init__(
        self,
        client: httpx.AsyncClient,
        params_converter: ParamsConverter = DefaultParamsConverter(),
    ):
        self._client = client
        self._params_converter = params_converter

    def call(self, api_request: ApiRequest) -> ApiResponse:
        methods = {
            "get": partial(self._read, self._client.get),
            "options": partial(self._read, self._client.options),
            "head": partial(self._read, self._client.head),
            "put": partial(self._write, self._client.put),
            "delete": partial(self._write, self._client.delete),
            "patch": partial(self._write, self._client.patch),
            "post": partial(self._write, self._client.post),
        }
        return methods[api_request.method](api_request=api_request)

    async def _read(self, make_request, api_request: ApiRequest):
        return await self._make_response(
            await make_request(
                url=api_request.path,
                params=self._params_converter.convert_query_params(
                    api_request.query_params
                ),
                headers=api_request.headers,
                cookies=api_request.cookies,
            )
        )

    async def _write(self, make_request, api_request: ApiRequest):
        params = dict(
            url=api_request.path,
            headers=api_request.headers,
            cookies=api_request.cookies,
        )

        if api_request.content_type == APPLICATION_JSON:
            params["json"] = api_request.body
        else:
            params["data"] = api_request.body

        return await self._make_response(await make_request(**params))

    async def _make_response(self, response: httpx.Response) -> ApiResponse:
        try:
            body = response.json()
        except ValueError:
            body = response.content

        return ApiResponse(
            url=str(response.url),
            body=body,
            headers=dict(response.headers),
            status_code=response.status_code,
            content_type=response.headers["Content-Type"],
        )
