from enum import StrEnum


class CardType(StrEnum):
    SCRIPT_PAYLOAD = 'Script Payload'
    SCRIPT_MOD = 'Script Mod'
    SCRIPT_VECTOR = 'Script Vector'
    WARD = 'Ward'
    UTILITY = 'Utility'
    NULL = 'Null'

