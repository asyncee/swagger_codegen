from dataclasses import dataclass
from dataclasses import field
from typing import Dict


@dataclass
class Configuration:
    host: str
    headers: Dict[str, str] = field(default_factory=dict)
