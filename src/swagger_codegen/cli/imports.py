import importlib
from typing import Type


def qualname(cls: Type) -> str:
    return cls.__module__ + "." + cls.__qualname__


def import_class(import_path):
    module_name, classname = import_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, classname)
