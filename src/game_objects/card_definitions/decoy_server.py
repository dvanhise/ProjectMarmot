from src.game_objects.card_type import CardType
from src.game_objects.tags.cardmine import CardMine
from src.game_objects.vector import Vector
from src.game_objects.card import Card
from src.game_objects.tags.vector import Vector as VectorTag



class DecoyServer(Card):
    id = 'decoy-server'
    name = 'Decoy Server'
    type = CardType.SCRIPT_VECTOR
    rarity = 'simple'
    tooltips = [VectorTag, CardMine]
    image_id = 'decoy-server'
    cost = 1
    description = ['Install Vector:', '  On capture,', '  shuffle Lance', '  into draw pile']
    vector = Vector(name='Decoy', tags=[CardMine(count=1, card='lance')])
