from typing import List

from dataclasses import dataclass

from swagger_codegen.parsing.endpoint import EndpointDescription


@dataclass
class Api:
    name: str
    type_name: str
    endpoints: List[EndpointDescription]
