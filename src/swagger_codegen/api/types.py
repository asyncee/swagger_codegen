from typing import Callable, Dict, Literal, Optional, Tuple, Union

from schemathesis import types


class _GenericAlias:
    __args__: Tuple


Body = types.Body
Query = types.Query
Headers = types.Headers
PathParameters = types.PathParameters
Cookies = types.Cookies
FormData = types.FormData
StatusCode = int
MaybeDefaultStatusCode = Union[Literal["default"], str]
ContentType = str
ResponseType = Optional[Union[_GenericAlias, Callable]]
ResponseMapping = Dict[MaybeDefaultStatusCode, Dict[ContentType, ResponseType]]
APPLICATION_JSON: str = "application/json"
