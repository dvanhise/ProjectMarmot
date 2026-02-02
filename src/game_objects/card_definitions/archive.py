from game_objects.card_type import CardType
from utils.action_queue import get_aq
from game_objects.card import Card


class Archive(Card):
    id = 'archive'
    name = 'Archive'
    type = CardType.UTILITY
    rarity = 'simple'
    image_id = 'query',
    cost = 1
    description = ['Delete right-most card,', 'draw 2 cards']

    def on_play(self):
        get_aq().queue_action('delete_card', 'RIGHT', 1)
        get_aq().queue_action('draw_cards', 2)
