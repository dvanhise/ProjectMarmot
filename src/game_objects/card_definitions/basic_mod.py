from game_objects.game_state import GameState
from game_objects.script import Script
from game_objects.card_type import CardType


def on_script_activation(script: Script):
    script.power += 2


definition = {
    'id': 'basic-mod',
    'name': 'Boost',
    'type': CardType.SCRIPT_MOD,
    'cost': 1,
    'description': '+2 power',
    'rarity': 'TODO',
    'on_play': None,
    'vector': None,
    'on_script_add': None,
    'on_script_activation': on_script_activation,
    'on_ward_install': None,
    'image_id': 'mod'
}


