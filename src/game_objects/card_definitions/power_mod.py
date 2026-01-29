from game_objects.script import Script
from game_objects.card_type import CardType


def on_script_activation(script: Script):
    script.power += 3


definition = {
    'id': 'power-mod',
    'name': 'Power Mod',
    'type': CardType.SCRIPT_MOD,
    'rarity': 'simple',
    'image_id': 'mod',
    'cost': 1,
    'description': '3 Power',
    'on_script_activation': on_script_activation
}


