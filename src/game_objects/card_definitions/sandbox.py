from game_objects.card_type import CardType
from utils.action_queue import get_aq
from game_objects.card import Card
from game_objects.tags.delayed_draw import DelayedDraw
from game_objects.tags.fortify import Fortify


class Sandbox(Card):
    id = 'sandbox'
    name = 'Sandbox'
    type = CardType.WARD
    rarity = 'intermediate'
    tooltips = [Fortify]
    image_id = 'query',
    cost = 3
    description = ['Apply Fortify 1,', 'next turn draw 2 cards']

    def on_play(self):
        get_aq().queue_action('add_player_tag', DelayedDraw, 2)

    def on_ward_install(self, node):
        node.tags.add_tag(Fortify(1))
