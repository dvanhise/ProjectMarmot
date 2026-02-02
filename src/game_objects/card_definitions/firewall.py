from game_objects.tags.netburn import NetBurn
from game_objects.card_type import CardType
from game_objects.card import Card


class Firewall(Card):
    id = 'firewall'
    name = 'Firewall'
    type = CardType.WARD
    rarity = 'simple'
    image_id = 'ward',
    cost = 1
    description = ['{ward} ward, netburn']
    ward = 6

    def on_ward_install(self, node):
        node.apply_ward(self.ward)
        node.tags.add_tag(NetBurn(1))
