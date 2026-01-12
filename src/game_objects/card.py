from dataclasses import dataclass
from typing import Callable
from game_objects.card_type import CardType


@dataclass
class Card:
    name: str
    type: CardType
    cost: int
    description: str
    rarity: str
    image_id: str
    on_play: Callable = None
    on_vector_install: Callable = None
    on_script_add: Callable = None
    on_script_activation: Callable = None
    on_ward_install: Callable = None
