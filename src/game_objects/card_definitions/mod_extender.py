from src.game_objects.card_type import CardType
from src.utils.action_queue import get_aq
from src.game_objects.card import Card


class ModExtender(Card):
    id = 'mod-extender'
    name = 'Mod Extender'
    type = CardType.UTILITY
    rarity = 'elite'
    image_id = 'query'
    cost = 1
    description = ['Gain an additional', 'mod slot', 'delete']
    delete_on_play = True

    def on_play(self):
        get_aq().queue_action('add_script_slot', CardType.SCRIPT_MOD)
