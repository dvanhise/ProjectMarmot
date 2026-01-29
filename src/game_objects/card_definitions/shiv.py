from game_objects.script import Script
from game_objects.card_type import CardType


def on_script_activation(script: Script):
    script.power += 2


definition = {
    'id': 'shiv',
    'name': 'Shiv',
    'type': CardType.SCRIPT_PAYLOAD,
    'rarity': 'simple',
    'image_id': 'payload',
    'cost': 0,
    'description': '2 Power',
    'on_script_activation': on_script_activation
}


