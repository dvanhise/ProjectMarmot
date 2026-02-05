from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.ward import Ward



class Bulwark(Card):
    id = 'bulwark'
    name = 'Bulwark'
    type = CardType.WARD
    rarity = 'simple'
    image_id = 'bulwark'
    tooltips = [Ward]
    cost = 1
    description = ['Ward {ward}']
    ward = 3
    delete_on_play = True

    def on_ward_install(self, node):
        node.apply_ward(self.ward)
