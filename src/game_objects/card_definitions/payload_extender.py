from game_objects.card_type import CardType
from utils.action_queue import get_aq
from game_objects.card import Card


class PayloadExtender(Card):
    id = 'payload-extender'
    name = 'Payload Extender'
    type = CardType.UTILITY
    rarity = 'elite'
    image_id = 'query',
    cost = 1
    description = ['Gain an additional', 'payload slot', 'delete']

    def on_play(self):
        get_aq().queue_action('add_script_slot', CardType.SCRIPT_PAYLOAD)
