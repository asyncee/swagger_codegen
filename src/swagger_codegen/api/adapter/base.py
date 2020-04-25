import abc

from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api.response import ApiResponse


class HttpClientAdapter(abc.ABC):
    @abc.abstractmethod
    def call(self, api_request: ApiRequest) -> ApiResponse:
        pass
