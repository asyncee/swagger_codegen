from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from swagger_codegen.api.types import Body
from swagger_codegen.api.types import ContentType
from swagger_codegen.api.types import Cookies
from swagger_codegen.api.types import Headers
from swagger_codegen.api.types import Query


@dataclass
class ApiRequest:
    method: str
    path: str
    content_type: Optional[ContentType] = None
    body: Optional[Body] = None
    headers: Headers = field(default_factory=dict)
    query_params: Query = field(default_factory=dict)
    cookies: Cookies = field(default_factory=dict)

    def __post_init__(self):
        self.method = self.method.lower()

    def clone(self, **params):
        return self.__class__(**{**asdict(self), **params})
