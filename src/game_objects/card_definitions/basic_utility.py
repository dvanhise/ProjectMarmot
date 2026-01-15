from game_objects.player import Player
from game_objects.card_type import CardType


def on_play(player: Player):
    player.deck.draw(3)


definition = {
    'id': 'basic-utility',
    'name': 'Query',
    'type': CardType.UTILITY,
    'cost': 1,
    'description': 'Draw 3 cards',
    'rarity': 'TODO',
    'on_play': on_play,
    'image_id': 'query'
}


