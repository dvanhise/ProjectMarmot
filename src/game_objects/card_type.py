from enum import StrEnum, auto


class CardType(StrEnum):
    SCRIPT_PAYLOAD = auto()
    SCRIPT_MOD = auto()
    SCRIPT_VECTOR = auto()
    WARD = auto()
    UTILITY = auto()
