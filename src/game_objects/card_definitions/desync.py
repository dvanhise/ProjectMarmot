from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.delayed_energy import DelayedEnergy
from utils.action_queue import get_aq


class Desync(Card):
    id = 'desync'
    name = 'Desync'
    type = CardType.WARD
    rarity = 'simple'
    image_id = 'ward',
    cost = 1
    description = ['{ward} ward,', 'next turn', 'gain 1 energy']
    ward = 2

    def on_ward_install(self, node):
        node.apply_ward(self.ward)
        get_aq().queue_action('add_player_tag', DelayedEnergy, 1)
