from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.selfbuilding import SelfBuilding
from game_objects.tags.ward import Ward


class DefensiveNanobots(Card):
    id = 'defensive-nanobots'
    name = 'Defensive Nanobots'
    type = CardType.WARD
    rarity = 'simple'
    tooltips = [SelfBuilding, Ward]
    image_id = 'query',
    cost = 1
    description = ['Apply Self-Building 1']

    def on_ward_install(self, node):
        node.tags.add_tag(SelfBuilding(1))
