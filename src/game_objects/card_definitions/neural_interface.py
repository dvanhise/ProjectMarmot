from game_objects.player import Player
from game_objects.card_type import CardType


def on_play(player: Player):
    player.health -= 1
    player.energy += 2
    # TODO: Figure out how to do something with script builder


definition = {
    'id': 'neural-interface',
    'name': 'Neutal Interface',
    'type': CardType.UTILITY,
    'rarity': 'intermediate',
    'image_id': 'query',
    'cost': 0,
    'description': ['Take 1 damage', 'Gain 2 energy', 'Execute script for free'],
    'on_play': on_play
}


