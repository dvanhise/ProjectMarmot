from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.selfbuilding import SelfBuilding


class DefensiveNanobots(Card):
    id = 'defensive-nanobots'
    name = 'Defensive Nanobots'
    type = CardType.WARD
    rarity = 'simple'
    image_id = 'query',
    cost = 1
    description = ['Apply 1 self-building']

    def on_ward_install(self, node):
        node.tags.add_tag(SelfBuilding(1))
