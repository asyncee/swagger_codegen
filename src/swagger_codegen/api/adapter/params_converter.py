import abc
import datetime as dt
from typing import Any
from typing import Callable
from typing import Dict
from typing import MutableMapping
from typing import Optional
from typing import Type
from typing import TypeVar

from multidict import MultiDict

T = TypeVar("T")


class ParamsConverter(abc.ABC):
    @abc.abstractmethod
    def convert_query_params(self, params: Dict[str, Any]) -> Dict[str, str]:
        pass


class DefaultParamsConverter(ParamsConverter):
    def __init__(
        self, handlers: Optional[Dict[Type[T], Callable[[Dict, str, T], None]]] = None
    ):
        handlers = handlers or {}
        default_handlers = {
            list: self.handle_list,
            tuple: self.handle_tuple,
            type(None): self.handle_none,
            dt.datetime: self.handle_datetime,
            dt.date: self.handle_date,
        }
        self.handlers = {**default_handlers, **handlers}

    def convert_query_params(self, params: Dict[str, Any]) -> MutableMapping[str, str]:
        result = self.get_result_container()

        for k, v in params.items():
            handler = self.handlers.get(type(v))
            if not handler:
                self.handle_unknown(result, k, v)
            else:
                handler(result, k, v)

        return result

    def get_result_container(self) -> MutableMapping:
        return {}

    def handle_none(self, result: MutableMapping, key: str, value):
        # Do not serialize None to query parameters.
        pass

    def handle_list(self, result: MutableMapping, key: str, value: list):
        result[key] = value

    def handle_tuple(self, result: MutableMapping, key: str, value: tuple):
        return self.handle_list(result, key, list(value))

    def handle_datetime(self, result: MutableMapping, key: str, value: dt.datetime):
        result[key] = value.isoformat()

    def handle_date(self, result: MutableMapping, key: str, value: dt.date):
        result[key] = value.isoformat()

    def handle_unknown(self, result: MutableMapping, key: str, value: Any):
        result[key] = value


class AiohttpParamsConverter(DefaultParamsConverter):
    """
    Convert regular dict into aiohttp-specific MultiDict.

    Aiohttp does not support list or tuple parameters,
    so values of such parameters must be added one-by-one
    via MultiDict.add.
    """

    def get_result_container(self) -> MutableMapping:
        return MultiDict()

    def handle_list(self, result: MutableMapping, key: str, value: list):
        for el in value:
            result.add(key, el)
