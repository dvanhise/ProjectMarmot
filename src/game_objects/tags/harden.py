from game_objects.tag import Tag
from game_objects.card_type import CardType
from utils.action_queue import get_aq


class Harden(Tag):
    id = 'harden'
    icon = 'power'
    tooltip = 'Increases all card ward values by {count}.'

    def on_change(self, change):
        get_aq().queue_action('card_updates_ward', change)

    def on_temp_card_creation(self, card):
        if card.type == CardType.WARD and card.ward:
            card.ward += self.count
