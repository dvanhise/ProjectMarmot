from game_objects.card_type import CardType
from utils.action_queue import get_aq
from game_objects.card import Card


class NeuralInterface(Card):
    id = 'neural-interface'
    name = 'Neutal Interface'
    type = CardType.UTILITY
    rarity = 'intermediate'
    image_id = 'query',
    cost = 0
    description = ['Take 1 damage', 'Gain 2 energy', 'Execute script for free']

    def on_play(self):
        queue = get_aq()
        queue.queue_action('change_player_health', -1)
        queue.queue_action('change_energy', 2)
        queue.queue_action('execute_script')
