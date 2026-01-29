from game_objects.script import Script
from game_objects.card_type import CardType


def on_script_activation(script: Script):
    script.power += 6


definition = {
    'id': 'halberd',
    'name': 'Halberd',
    'type': CardType.SCRIPT_PAYLOAD,
    'rarity': 'simple',
    'image_id': 'payload',
    'cost': 2,
    'description': '6 Power',
    'on_script_activation': on_script_activation
}


