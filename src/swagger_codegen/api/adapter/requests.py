from functools import partial

import requests

from swagger_codegen.api.adapter.base import HttpClientAdapter
from swagger_codegen.api.adapter.params_converter import DefaultParamsConverter
from swagger_codegen.api.adapter.params_converter import ParamsConverter
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api.response import ApiResponse
from swagger_codegen.api.types import APPLICATION_JSON


class RequestsAdapter(HttpClientAdapter):
    def __init__(
        self,
        session: requests.Session = None,
        params_converter: ParamsConverter = DefaultParamsConverter(),
        debug: bool = False,
    ):
        self._session = session or requests.Session()
        self._params_converter = params_converter
        if debug:
            self._enable_debug()

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

    def _read(self, make_request, api_request: ApiRequest):
        response = make_request(
            url=api_request.path,
            params=self._params_converter.convert_query_params(
                api_request.query_params
            ),
            headers=api_request.headers,
            cookies=api_request.cookies,
        )
        return self._response(response)

    def _write(self, make_request, api_request: ApiRequest):
        params = dict(
            url=api_request.path,
            headers=api_request.headers,
            cookies=api_request.cookies,
        )

        if api_request.content_type == APPLICATION_JSON:
            params["json"] = api_request.body
        else:
            params["data"] = api_request.body

        return self._response(make_request(**params))

    def _response(self, response: requests.Response) -> ApiResponse:
        try:
            body = response.json()
        except ValueError:
            body = response.content

        return ApiResponse(
            url=response.url,
            body=body,
            headers=dict(response.headers),
            status_code=response.status_code,
            content_type=response.headers["Content-Type"],
        )

    def _enable_debug(self):
        from requests_toolbelt.utils import dump

        def logging_hook(response, *args, **kwargs):
            data = dump.dump_all(response)
            print(data.decode("utf-8"))

        self._session.hooks["response"] = [logging_hook]
