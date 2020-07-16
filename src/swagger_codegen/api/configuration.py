import enum
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Literal

from swagger_codegen.api.request import ApiRequest


class Hook(enum.Enum):
    request = "request"


RequestHook = Callable[[ApiRequest], ApiRequest]
RequestHooks = List[RequestHook]
Hooks = Dict[Literal[Hook.request], RequestHooks]


@dataclass
class Configuration:
    """
    Api client configuration.

    Arguments:
          host - Host to connect to.
          hooks - Registry of hooks that will be executed for an api request.

    Usage example:

    ```python
    from swagger_codegen.api.configuration import Hook

    def add_api_key(request: ApiRequest) -> ApiRequest:
        return request.clone(headers=dict(request.headers, **{'ApiKey': 'abcd'}))

    configuration=Configuration(
        host=host, hooks={Hook.request: [add_api_key]}
    )
    ```
    """

    host: str
    hooks: Hooks = field(default_factory=dict)
