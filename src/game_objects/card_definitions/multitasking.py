from src.game_objects.card_type import CardType
from src.game_objects.tags.multitasking import Multitasking as MultitaskingTag
from src.utils.action_queue import get_aq
from src.game_objects.card import Card


class Multitasking(Card):
    id = 'multitasking'
    name = 'Multi-tasking'
    type = CardType.UTILITY
    rarity = 'simple'
    image_id = 'query'
    cost = 1
    description = ['When executing a script', 'this encounter,', 'draw 1 card.']

    def on_play(self):
        get_aq().queue_action('add_player_tag', MultitaskingTag, 1)
