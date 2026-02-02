from game_objects.card_type import CardType
from utils.action_queue import get_aq
from game_objects.card import Card
from game_objects.tags.harden import Harden


class Patch(Card):
    id = 'patch'
    name = 'Patch'
    type = CardType.UTILITY
    rarity = 'intermediate'
    image_id = 'query',
    cost = 1
    description = ['Increase all ward', 'values by 1']

    def on_play(self):
        get_aq().queue_action('add_player_tag', Harden, 1)
