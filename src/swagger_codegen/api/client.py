from typing import Coroutine
from typing import Union

from swagger_codegen.api.adapter.base import HttpClientAdapter
from swagger_codegen.api.configuration import Configuration
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api.response import ApiResponse


class ApiClient:
    def __init__(self, configuration: Configuration, adapter: HttpClientAdapter):
        self._configuration = configuration
        self._adapter = adapter

    def call_api(
        self, api_request: ApiRequest
    ) -> Union[ApiResponse, Coroutine[None, None, ApiResponse]]:
        method = api_request.clone(
            path=self._configuration.host + api_request.path,
        )
        return self._adapter.call(method)
