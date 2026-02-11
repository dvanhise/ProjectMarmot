from src.game_objects.card_type import CardType
from src.game_objects.card import Card


class Override(Card):
    id = 'override'
    name = 'Override'
    type = CardType.SCRIPT_MOD
    rarity = 'elite'
    image_id = 'query'
    cost = 2
    description = ['Convert enemy vectors', 'on defeated nodes']

    def on_script_activation(self, script, player_info):
        script.destroy_vector_on_capture = False

