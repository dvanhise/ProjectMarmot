from game_objects.script import Script
from game_objects.card_type import CardType


def on_script_activation(script: Script):
    script.power += 6


definition = {
    'id': 'lance',
    'name': 'Lance',
    'type': CardType.SCRIPT_PAYLOAD,
    'rarity': 'special',
    'image_id': 'payload',
    'cost': 0,
    'description': ['6 Power', 'Delete when executed'],
    'delete_on_execution': True,
    'on_script_activation': on_script_activation
}


