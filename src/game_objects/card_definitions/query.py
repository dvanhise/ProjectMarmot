from game_objects.player import Player
from game_objects.card_type import CardType


def on_play(player: Player):
    player.draw(3)


definition = {
    'id': 'query',
    'name': 'Query',
    'type': CardType.UTILITY,
    'rarity': 'default',
    'image_id': 'query',
    'cost': 1,
    'description': 'Draw 3 cards',
    'on_play': on_play
}


