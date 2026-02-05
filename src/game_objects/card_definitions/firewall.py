from game_objects.tags.netburn import NetBurn
from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.ward import Ward


class Firewall(Card):
    id = 'firewall'
    name = 'Firewall'
    type = CardType.WARD
    rarity = 'simple'
    tooltips = [Ward, NetBurn]
    image_id = 'firewall'
    cost = 1
    description = ['{ward} Ward', 'Netburn 1']
    ward = 6

    def on_ward_install(self, node):
        node.apply_ward(self.ward)
        node.tags.add_tag(NetBurn(1))
