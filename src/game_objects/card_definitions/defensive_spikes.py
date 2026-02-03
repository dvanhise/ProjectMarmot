from game_objects.card_type import CardType
from game_objects.vector import Vector
from game_objects.tags.fortify import Fortify
from game_objects.card import Card


class DefensiveSpikes(Card):
    id = 'defensive-spikes'
    name = 'Defensive Spikes'
    type = CardType.SCRIPT_VECTOR
    rarity = 'intermediate'
    cost = 1
    description = ['Install Vector:', '  Has Ablative Spikes']
    vector = Vector(name='Spike', default_ward=1, tags=[Fortify(1)])
