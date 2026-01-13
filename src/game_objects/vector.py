from dataclasses import dataclass
from typing import Callable


@dataclass
class Vector:
    name: str
    power: int
    on_trigger: Callable = None
    on_install: Callable = None
    on_attack: Callable = None
