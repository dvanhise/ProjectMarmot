from src.game_objects.script import Script
from src.game_objects.card_type import CardType
from src.game_objects.card import Card
from src.game_objects.tags.power import Power


class Spike(Card):
    id = 'spike'
    name = 'Spike'
    type = CardType.SCRIPT_PAYLOAD
    rarity = 'built-in'
    tooltips = [Power]
    image_id = 'payload'
    cost = 1
    power = 3
    description = ['{power} Power']

    def on_script_activation(self, script: Script, player_info):
        script.power += self.power
