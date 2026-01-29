from game_objects.script import Script
from game_objects.card_type import CardType


def on_script_activation(script: Script):
    script.power += 3


definition = {
    'id': 'spike',
    'name': 'Spike',
    'type': CardType.SCRIPT_PAYLOAD,
    'rarity': 'default',
    'image_id': 'payload',
    'cost': 1,
    'description': '3 Power',
    'on_script_activation': on_script_activation
}


