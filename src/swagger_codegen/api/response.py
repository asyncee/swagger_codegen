from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from swagger_codegen.api.types import Body
from swagger_codegen.api.types import ContentType
from swagger_codegen.api.types import Headers
from swagger_codegen.api.types import StatusCode


@dataclass
class ApiResponse:
    url: str
    status_code: StatusCode
    content_type: ContentType
    body: Optional[Body]
    headers: Headers = field(default_factory=dict)

    def is_error(self):
        return self.status_code >= 400
