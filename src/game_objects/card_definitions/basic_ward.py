from game_objects.level import Node
from game_objects.card_type import CardType


def on_ward_install(node: Node):
    node.ward += 2


definition = {
    'id': 'basic-ward',
    'name': 'Security Group',
    'type': CardType.WARD,
    'cost': 1,
    'description': 'Add 2 ward',
    'rarity': 'TODO',
    'on_play': None,
    'vector': None,
    'on_script_add': None,
    'on_script_activation': None,
    'on_ward_install': on_ward_install,
    'image_id': 'ward'
}
