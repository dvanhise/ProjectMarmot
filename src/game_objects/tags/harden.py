from src.game_objects.tag import Tag
from src.game_objects.card_type import CardType
from src.utils.action_queue import get_aq


class Harden(Tag):
    id = 'harden'
    name = 'Harden'
    icon = 'harden'
    tooltip = 'Increase all card ward values by {count}.'

    def on_change(self, change):
        get_aq().queue_action('card_updates_ward', change)

    def on_temp_card_creation(self, card, player_info):
        if card.type == CardType.WARD and card.ward:
            card.ward += self.count
