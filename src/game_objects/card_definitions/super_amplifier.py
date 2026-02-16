from src.game_objects.card_type import CardType
from src.game_objects.vector import Vector
from src.game_objects.tags.boost import Boost
from src.game_objects.card import Card
from src.game_objects.tags.vector import Vector as VectorTag


class SuperAmplifier(Card):
    id = 'super-amplifier'
    name = 'Super Amplifier'
    type = CardType.SCRIPT_VECTOR
    rarity = 'intermediate'
    tooltips = [Vector, Boost]
    cost = 1
    description = ['Install Vector:', '  Boost 3']
    vector = Vector(name='B Amp', default_ward=0, tags=[Boost(3)])
