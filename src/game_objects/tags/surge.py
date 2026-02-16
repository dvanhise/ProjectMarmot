from src.game_objects.tag import Tag
from src.game_objects.card_type import CardType
from src.utils.action_queue import get_aq


class Surge(Tag):
    id = 'surge'
    name = 'Surge'
    icon = 'surge'
    tooltip = 'Increase all payload power by {count}.'

    def on_change(self, change):
        get_aq().queue_action('card_updates_power', change)

    def on_temp_card_creation(self, card, player_info):
        if card.type == CardType.SCRIPT_PAYLOAD and card.power:
            card.power += self.count
