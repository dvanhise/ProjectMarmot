from game_objects.card_type import CardType
from game_objects.vector import Vector
from game_objects.tags.boost import Boost
from game_objects.tags.vector import Vector as VectorTag
from game_objects.card import Card


class Amplifier(Card):
    id = 'amplifier'
    name = 'Amplifier'
    type = CardType.SCRIPT_VECTOR
    rarity = 'built-in'
    image_id = 'amplifier'
    cost = 1
    description = ['Install Vector:', '  Boost 2']
    tooltips = [VectorTag, Boost]
    vector = Vector(name='Amp', default_ward=0, tags=[Boost(2)])
