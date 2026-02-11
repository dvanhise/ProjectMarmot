from src.game_objects.card_type import CardType
from src.utils.action_queue import get_aq
from src.game_objects.card import Card
from src.game_objects.tags.harden import Harden
from src.game_objects.tags.ward import Ward


class Patch(Card):
    id = 'patch'
    name = 'Patch'
    type = CardType.UTILITY
    rarity = 'intermediate'
    tooltips = [Ward]
    image_id = 'query'
    delete_on_play = True
    cost = 2
    description = ['Increase all ward', 'values by 1', 'during the encounter.', 'Delete when played']

    def on_play(self):
        get_aq().queue_action('add_player_tag', Harden, 1)
