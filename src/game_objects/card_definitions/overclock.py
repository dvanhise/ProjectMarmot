from game_objects.card_type import CardType
from utils.action_queue import get_aq
from game_objects.card import Card
from game_objects.tags.surge import Surge
from game_objects.tags.power import Power


class Overclock(Card):
    id = 'overclock'
    name = 'Overclock'
    type = CardType.UTILITY
    rarity = 'intermediate'
    tooltips = [Power]
    image_id = 'query'
    delete_on_play = True
    cost = 2
    description = ['Increase all payload', 'power by 1', 'during the encounter.', 'Delete when played']

    def on_play(self):
        get_aq().queue_action('add_player_tag', Surge, 1)
