from unittest import mock

from pydantic import BaseModel
from swagger_codegen.api.base import BaseApi
from swagger_codegen.api.client import ApiClient
from swagger_codegen.api.configuration import Configuration
from swagger_codegen.api.exceptions import ErrorApiResponse
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api.response import ApiResponse
from swagger_codegen.parsing.endpoint import EndpointDescription
from swagger_codegen.parsing.loaders import load_base_schema
from swagger_codegen.parsing.parse import endpoints_from_base_schema


class ResponseA(BaseModel):
    message: str


class ResponseB(BaseModel):
    message: str


def test_response_mapping_for_multiple_responses():
    base_schema = load_base_schema("tests/fixtures/test_openapi.json")
    endpoints = endpoints_from_base_schema(base_schema, EndpointDescription)
    endpoint = next((e for e in endpoints if e.path == "/multiple-status-codes"), None)
    assert endpoint.response_mapping == {
        "200": {"application/json": "ResponseA"},
        "400": {"default": "None"},
        "422": {"application/json": "ResponseB"},
    }


def test_multiple_responses():
    response_200 = ApiResponse(
        url="/multiple-status-codes",
        status_code=200,
        content_type="application/json",
        body={"message": "response-a"},
        headers={},
    )
    response_400 = ApiResponse(
        url="/multiple-status-codes",
        status_code=400,
        content_type="application/json",
        body=None,
        headers={},
    )

    adapter = mock.Mock()
    adapter.call = mock.Mock(return_value=response_400)

    configuration = Configuration(host="")
    client = ApiClient(configuration, adapter)
    api = BaseApi(client, configuration)
    request = ApiRequest(
        method="GET",
        path="/multiple-status-codes",
        content_type=None,
        body=None,
        headers={},
        query_params={},
        cookies={},
    )

    response_mapping = {
        "200": {"application/json": ResponseA},
        "400": {"default": None},
        "422": {"application/json": ResponseB},
    }

    # 400
    try:
        api.make_request(response_mapping, request)
    except ErrorApiResponse as e:
        assert e.request == request
        assert e.response == response_400
        assert e.response_body is None

    # 200
    adapter.call = mock.Mock(return_value=response_200)
    assert api.make_request(response_mapping, request) == ResponseA(
        message="response-a"
    )
