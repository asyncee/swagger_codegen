import inspect
import logging
from typing import Optional

from swagger_codegen.api.client import ApiClient
from swagger_codegen.api.configuration import Configuration
from swagger_codegen.api.configuration import Hook
from swagger_codegen.api.exceptions import ErrorApiResponse
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api.response import ApiResponse
from swagger_codegen.api.response_deserializer import DefaultResponseDeserializer
from swagger_codegen.api.response_deserializer import ResponseDeserializer
from swagger_codegen.api.types import ResponseMapping
from swagger_codegen.api.types import ResponseType

logger = logging.getLogger(__name__)


class BaseApi:
    def __init__(
        self,
        client: ApiClient,
        configuration: Configuration,
        raise_for_status: bool = True,
        deserializer: ResponseDeserializer = DefaultResponseDeserializer(),
    ):
        self._client = client
        self._configuration = configuration
        self._raise_for_status = raise_for_status
        self._deserializer = deserializer

    def make_request(self, response_mapping: ResponseMapping, api_request: ApiRequest):
        for request_hook in self._configuration.hooks.get(Hook.request, []):
            api_request = request_hook(api_request)

        result = self._client.call_api(api_request)

        if inspect.iscoroutine(result):

            async def _wrap_coroutine():
                api_response = await result
                return self._handle_result(response_mapping, api_request, api_response)

            return _wrap_coroutine()

        return self._handle_result(response_mapping, api_request, result)

    def _handle_result(
        self,
        response_mapping: ResponseMapping,
        api_request: ApiRequest,
        api_response: ApiResponse,
    ):
        response_type = self._select_response_type(response_mapping, api_response)
        deserialized_response = self._deserializer.deserialize(
            response_type, api_response.body
        )
        if self._raise_for_status and api_response.is_error() >= 400:
            raise ErrorApiResponse(api_request, api_response, deserialized_response)

        return deserialized_response

    def _select_response_type(
        self, response_mapping: ResponseMapping, response: ApiResponse,
    ) -> Optional[ResponseType]:
        content_types = response_mapping.get(
            str(response.status_code)
        ) or response_mapping.get("default")
        if content_types is None:
            return None
        return content_types.get(response.content_type)

    def _only_provided(self, dct: dict) -> dict:
        return {k: v for k, v in dct.items() if v is not ...}
