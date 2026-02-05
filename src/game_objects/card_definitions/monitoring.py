from game_objects.card_type import CardType
from game_objects.tags.bandwidth import Bandwidth
from utils.action_queue import get_aq
from game_objects.card import Card


class Monitoring(Card):
    id = 'monitoring'
    name = 'Monitoring'
    type = CardType.UTILITY
    rarity = 'intermediate'
    image_id = 'query'
    cost = 1
    description = ['When a friendly node', 'is captured,', 'gain 1 energy']

    def on_play(self):
        get_aq().queue_action('add_player_tag', Bandwidth, 1)
