from game_objects.card_type import CardType
from game_objects.vector import Vector
from game_objects.tags.boost import Boost


definition = {
    'id': 'amplifier',
    'name': 'Amplifier',
    'type': CardType.SCRIPT_VECTOR,
    'rarity': 'default',
    'image_id': 'default',
    'cost': 1,
    'description': ['Install Vector:', '  Boost script power +2'],
    'vector': Vector(name='Amp', default_ward=0, tags=[Boost(2)])
}


