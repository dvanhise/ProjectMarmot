from src.game_objects.card_type import CardType
from src.game_objects.tags.bandwidth import Bandwidth
from src.utils.action_queue import get_aq
from src.game_objects.card import Card


class Monitoring(Card):
    id = 'monitoring'
    name = 'Monitoring'
    type = CardType.UTILITY
    rarity = 'intermediate'
    image_id = 'query'
    cost = 1
    description = ['During this encounter,', 'gain 1 energy', 'when a friendly node', 'is captured.', 'Delete when played.']
    delete_on_play = True

    def on_play(self):
        get_aq().queue_action('add_player_tag', Bandwidth, 1)
