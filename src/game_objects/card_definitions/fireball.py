from game_objects.script import Script
from game_objects.tags.netburn import NetBurn
from game_objects.card_type import CardType


def on_script_activation(script: Script):
    script.tags.append(NetBurn(2))


definition = {
    'id': 'fireball',
    'name': 'Fireball',
    'type': CardType.SCRIPT_MOD,
    'rarity': 'simple',
    'image_id': 'mod',
    'cost': 0,
    'description': 'Add Netburn to payload',
    'on_script_activation': on_script_activation
}


