from src.game_objects.card_type import CardType
from src.utils.action_queue import get_aq
from src.game_objects.card import Card


class Query(Card):
    id = 'query'
    name = 'Query'
    type = CardType.UTILITY
    rarity = 'simple'
    image_id = 'query'
    cost = 1
    description = ['Draw 3 cards']

    def on_play(self):
        get_aq().queue_action('draw_cards', 3)
