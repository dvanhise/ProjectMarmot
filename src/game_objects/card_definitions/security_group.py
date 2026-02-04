from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.ward import Ward


class SecurityGroup(Card):
    id = 'security-group'
    name = 'Security Group'
    type = CardType.WARD
    rarity = 'built-in'
    tooltips = [Ward]
    image_id = 'ward',
    cost = 1
    description = ['Ward {ward}']
    ward = 2

    def on_ward_install(self, node):
        node.apply_ward(self.ward)