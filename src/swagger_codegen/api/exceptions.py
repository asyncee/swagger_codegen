from typing import Optional

from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api.response import ApiResponse
from swagger_codegen.api.types import Body


class ErrorApiResponse(Exception):
    """Raised when remote api respond with an error (4xx, 5xx)."""

    def __init__(
        self, request: ApiRequest, response: ApiResponse, response_body: Optional[Body]
    ):
        self.request = request
        self.response = response
        self.response_body = response_body
