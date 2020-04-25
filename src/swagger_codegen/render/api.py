from dataclasses import dataclass
from typing import List

from swagger_codegen.parsing.endpoint import EndpointDescription


@dataclass
class Api:
    name: str
    type_name: str
    endpoints: List[EndpointDescription]
