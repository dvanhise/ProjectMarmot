from game_objects.card_type import CardType
from game_objects.vector import Vector
from game_objects.tags.boost import Boost
from game_objects.tags.charge_up import ChargeUp
from game_objects.card import Card
from game_objects.tags.vector import Vector as VectorTag


class Overcharge(Card):
    id = 'overcharge'
    name = 'Overcharge'
    type = CardType.SCRIPT_VECTOR
    rarity = 'intermediate'
    tooltips = [VectorTag, Boost]
    cost = 1
    description = ['Install Vector:', '  Boost 2', '  On install,', '  use all energy(X),', '  gain 2*X Boost']
    vector = Vector(name='Amp', default_ward=0, tags=[Boost(2)])

    def on_script_activation(self, script, player_info):
        script.tags.add_tag(ChargeUp(1))
