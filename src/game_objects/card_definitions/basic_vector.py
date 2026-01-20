from game_objects.card_type import CardType
from game_objects.vector import Vector


definition = {
    'id': 'basic-vector',
    'name': 'Amplifier',
    'type': CardType.SCRIPT_VECTOR,
    'cost': 1,
    'description': 'Install vector TODO',
    'rarity': 'TODO',
    'vector': Vector(name='Amp', power_boost=2, default_ward=0),
    'image_id': 'default'
}


