from game_objects.card_type import CardType
from game_objects.tags.multitasking import Multitasking as MultitaskingTag
from utils.action_queue import get_aq
from game_objects.card import Card


class Multitasking(Card):
    id = 'multitasking'
    name = 'Multi-tasking'
    type = CardType.UTILITY
    rarity = 'intermediate'
    image_id = 'query',
    cost = 1
    description = ['When executing a script,', 'draw 1 card']

    def on_play(self):
        get_aq().queue_action('add_player_tag', MultitaskingTag, 1)
