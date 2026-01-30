from game_objects.card_type import CardType
from game_objects.tags.cardmine import CardMine
from game_objects.vector import Vector


definition = {
    'id': 'decoy_server',
    'name': 'Decoy Server',
    'type': CardType.SCRIPT_VECTOR,
    'rarity': 'simple',
    'image_id': 'vector',
    'cost': 1,
    'description': ['Install Vector:', '  On capture,', '  shuffle Lance', '  into draw pile'],
    'vector': Vector(name='Amp', tags=[CardMine(count=1, card='lance')])
}
