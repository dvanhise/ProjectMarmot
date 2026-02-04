from game_objects.card_type import CardType
from game_objects.vector import Vector
from game_objects.tags.fortify import Fortify
from game_objects.card import Card
from game_objects.tags.vector import Vector as VectorTag
from game_objects.tags.ward import Ward



class DefensiveSpikes(Card):
    id = 'defensive-spikes'
    name = 'Defensive Spikes'
    type = CardType.SCRIPT_VECTOR
    rarity = 'intermediate'
    tooltips = [VectorTag, Ward, Fortify]
    cost = 1
    description = ['Install Vector:', '  Ward 1', 'Fortify 1']
    vector = Vector(name='Spike', default_ward=1, tags=[Fortify(1)])
