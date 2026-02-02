from game_objects.card_type import CardType
from game_objects.vector import Vector
from game_objects.tags.boost import Boost
from game_objects.card import Card


class SuperAmplifier(Card):
    id = 'super-amplifier'
    name = 'Super Amplifier'
    type = CardType.SCRIPT_VECTOR
    rarity = 'intermediate'
    cost = 1
    description = ['Install Vector:', '  Boost script power +4']
    vector = Vector(name='Amp', default_ward=0, tags=[Boost(4)])
