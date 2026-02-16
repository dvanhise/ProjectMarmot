from src.game_objects.card_type import CardType
from src.game_objects.vector import Vector
from src.game_objects.tags.fortify import Fortify
from src.game_objects.card import Card
from src.game_objects.tags.vector import Vector as VectorTag
from src.game_objects.tags.ward import Ward


class Sandbox(Card):
    id = 'sandbox'
    name = 'Sandbox'
    type = CardType.SCRIPT_VECTOR
    rarity = 'intermediate'
    image_id = 'sandbox'
    tooltips = [VectorTag, Ward, Fortify]
    cost = 1
    description = ['Install Vector:', '  Ward 1', '  Fortify 1']
    vector = Vector(name='Spike', default_ward=1, tags=[Fortify(1)])

