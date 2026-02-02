from game_objects.card_type import CardType
from utils.action_queue import get_aq
from game_objects.card import Card
from game_objects.tags.surge import Surge


class Overclock(Card):
    id = 'overclock'
    name = 'Overclock'
    type = CardType.UTILITY
    rarity = 'intermediate'
    image_id = 'query',
    cost = 1
    description = ['Increase all payload', 'power by 1']

    def on_play(self):
        get_aq().queue_action('add_player_tag', Surge, 1)
