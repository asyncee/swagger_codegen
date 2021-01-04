from typing import Optional

from dataclasses import dataclass, field

from swagger_codegen.api.types import Body, ContentType, Headers, StatusCode


@dataclass
class ApiResponse:
    url: str
    status_code: StatusCode
    content_type: ContentType
    body: Optional[Body]
    headers: Headers = field(default_factory=dict)

    def is_error(self):
        return self.status_code >= 400
