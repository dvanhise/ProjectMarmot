from game_objects.game_state import GameState
from game_objects.script import Script
from game_objects.card_type import CardType


def on_script_activation(script: Script):
    pass


definition = {
    'name': 'Payload1',
    'type': CardType.SCRIPT_PAYLOAD,
    'cost': 1,
    'description': """
    4 %power%
    """,
    'rarity': 'TODO',
    'on_play': None,
    'on_vector_install': None,
    'on_script_add': None,
    'on_script_activation': on_script_activation,
    'on_ward_install': None,
    'image_id': 'temp'
}


