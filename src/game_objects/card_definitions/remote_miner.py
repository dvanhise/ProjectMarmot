from game_objects.script import Script
from game_objects.tags.energy_drain import EnergyDrain
from game_objects.card_type import CardType


def on_script_activation(script: Script):
    script.tags.append(EnergyDrain(1))


definition = {
    'id': 'remote-miner',
    'name': 'Fireball',
    'type': CardType.SCRIPT_MOD,
    'rarity': 'intermediate',
    'image_id': 'mod',
    'cost': 2,
    'description': ['Gain 1 energy for', 'each node captured'],
    'on_script_activation': on_script_activation
}


