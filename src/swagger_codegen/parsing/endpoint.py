from collections import defaultdict
from itertools import groupby
from typing import List
from typing import Optional

import attr
from inflection import underscore
from schemathesis.models import Endpoint

from swagger_codegen.parsing.data_type_parser import make_data_type
from swagger_codegen.parsing.endpoint_request import EndpointRequest
from swagger_codegen.parsing.endpoint_response import EndpointResponse


@attr.s(slots=True)
class EndpointDescription:
    endpoint: Endpoint = attr.ib()

    @property
    def tags(self):
        return self.endpoint.definition.get("tags", ["api"])

    @property
    def name(self):
        if "operationId" in self.endpoint.definition:
            return self.endpoint.definition["operationId"]
        return (
            f"{self.method}_{self.path}".lower()
            .replace("-", "_")
            .replace("/", "_")
            .replace("{", "")
            .replace("}", "")
        )

    @property
    def docstring(self) -> Optional[str]:
        return self.endpoint.definition.get("summary", None)

    @property
    def body_request(self) -> Optional[EndpointRequest]:
        name = "__request__"
        if self.endpoint.body:
            return EndpointRequest(
                name=name,
                data_type=make_data_type(self.endpoint.body),
                definition=self.endpoint.body,
                content_type="application/json",
            )
        if self.endpoint.form_data:
            return EndpointRequest(
                name=name,
                data_type=make_data_type(self.endpoint.form_data),
                definition=self.endpoint.form_data,
                content_type="multipart/form-data",
            )
        return None

    @property
    def responses(self) -> List[EndpointResponse]:
        _responses = []

        responses = list(self.endpoint.definition["responses"].items())
        default_response = self.endpoint.definition["responses"].get("default")

        if default_response and "content" in default_response:
            responses.extend(list(default_response.items()))

        for status_code, response_definition in responses:
            if "content" not in response_definition:
                empty_response = EndpointResponse(
                    status_code=status_code,
                    data_type=make_data_type({}),
                    definition={},
                    content_type="default",
                )
                if empty_response not in _responses:
                    _responses.append(empty_response)
                continue

            for content_type, response_schema in response_definition["content"].items():
                response = EndpointResponse(
                    status_code=status_code,
                    data_type=make_data_type(response_schema["schema"]),
                    definition=response_schema["schema"],
                    content_type=content_type,
                )
                if response not in _responses:
                    _responses.append(response)

        return sorted(_responses, key=lambda o: (o.status_code, o.content_type))

    @property
    def response_mapping(self):
        result = defaultdict(dict)
        for status_code, responses_by_status in groupby(
            self.responses, key=lambda o: o.status_code
        ):
            for response in responses_by_status:
                result[status_code][
                    response.content_type
                ] = response.data_type.python_type
        return dict(result)

    @property
    def return_type(self) -> str:
        response_types = sorted(
            set(
                [
                    r.data_type.python_type
                    for r in self.responses
                    if r.status_code.isdigit() and int(r.status_code) < 400
                ]
            ),
            key=lambda x: x,
        )

        if not response_types:
            return "None"

        if len(response_types) == 1:
            return list(response_types)[0]

        if len(response_types) == 2 and "None" in response_types:
            a, b = response_types
            return b if a == "None" else a

        alternative_types = ", ".join(response_types)
        return f"typing.Union[{alternative_types}]"

    @property
    def method(self):
        return self.endpoint.method

    @property
    def path(self):
        return self.endpoint.path

    @property
    def arguments(self):
        arguments_ = []

        containers = [
            self.endpoint.path_parameters,
            self.endpoint.headers,
            self.endpoint.cookies,
            self.endpoint.query,
            self.endpoint.form_data,
        ]

        for container in containers:
            if container is None:
                continue
            for parameter_name, parameter_body in container["properties"].items():
                is_required = parameter_name in container["required"]
                arguments_.append(
                    self.to_argument(parameter_name, parameter_body, is_required)
                )

        return sorted(arguments_, key=lambda arg: arg["required"] is False)

    def make_variable_name(self, original_name: str) -> str:
        return underscore(original_name.lower())

    def to_argument(self, name: str, schema: dict, is_required: bool):
        argument = {
            "name": name,
            "type": make_data_type(schema).python_type,
            "required": is_required,
        }
        default = schema.get("default")
        if default:
            argument["default"] = repr(default)
        if not is_required and "default" not in argument:
            argument["default"] = "..."
        return argument

    def to_arguments(self, items: dict):
        if not items:
            return []

        result = []

        for field_name, schema in items["properties"].items():
            is_required = field_name in items["required"]
            result.append(self.to_argument(field_name, schema, is_required))
        return result
