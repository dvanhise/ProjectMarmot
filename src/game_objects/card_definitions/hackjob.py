from game_objects.card_type import CardType
from game_objects.vector import Vector
from game_objects.tags.boost import Boost
from game_objects.tags.boost_loss import BoostLoss
from game_objects.card import Card


class Hackjob(Card):
    id = 'hackjob'
    name = 'Hackjob'
    type = CardType.SCRIPT_VECTOR
    rarity = 'simple'
    cost = 1
    description = ['Install Vector:', '  Boost 4', 'at end of turn', 'reduce boost by 1']
    vector = Vector(name='Hack', default_ward=0, tags=[Boost(4), BoostLoss(1)])
