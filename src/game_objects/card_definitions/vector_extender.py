from src.game_objects.card_type import CardType
from src.utils.action_queue import get_aq
from src.game_objects.card import Card


class VectorExtender(Card):
    id = 'vector-extender'
    name = 'Vector Extender'
    type = CardType.UTILITY
    rarity = 'elite'
    image_id = 'query'
    cost = 1
    description = ['Gain an additional', 'vector slot', 'delete']

    def on_play(self):
        get_aq().queue_action('add_script_slot', CardType.SCRIPT_VECTOR)
