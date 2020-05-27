import enum
from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Dict


class Hook(enum.Enum):
    request = 'request'


@dataclass
class Configuration:
    host: str
    hooks: Dict[Hook, Callable] = field(default_factory=dict)
