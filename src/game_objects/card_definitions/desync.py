from src.game_objects.card_type import CardType
from src.game_objects.card import Card
from src.game_objects.tags.delayed_energy import DelayedEnergy
from src.utils.action_queue import get_aq
from src.game_objects.tags.ward import Ward


class Desync(Card):
    id = 'desync'
    name = 'Desync'
    type = CardType.WARD
    rarity = 'simple'
    image_id = 'desync'
    tooltips = [Ward]
    cost = 1
    description = ['{ward} Ward.', 'Gain 1 energy next turn.']
    ward = 2

    def on_ward_install(self, node):
        node.apply_ward(self.ward)
        get_aq().queue_action('add_player_tag', DelayedEnergy, 1)
