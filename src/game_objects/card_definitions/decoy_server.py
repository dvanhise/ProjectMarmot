from game_objects.card_type import CardType
from game_objects.tags.cardmine import CardMine
from game_objects.vector import Vector
from game_objects.card import Card


class DecoyServer(Card):
    id = 'decoy_server'
    name = 'Decoy Server'
    type = CardType.SCRIPT_VECTOR
    rarity = 'simple'
    image_id = 'vector',
    cost = 1
    description = ['Install Vector:', '  On capture,', '  shuffle Lance', '  into draw pile']
    vector = Vector(name='Decoy', tags=[CardMine(count=1, card='lance')])
