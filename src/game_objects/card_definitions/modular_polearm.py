from src.game_objects.script import Script
from src.game_objects.card_type import CardType
from src.game_objects.card import Card
from src.game_objects.tags.power import Power


class ModularPolearm(Card):
    id = 'modulear-polearm'
    name = 'Modulear Polarm'
    type = CardType.SCRIPT_PAYLOAD
    rarity = 'intermediate'
    tooltips = [Power]
    image_id = 'payload'
    cost = 1
    power = 2
    description = ['{power} Power.', 'Increase power by 1', 'when replacing a', 'script payload']

    def on_script_activation(self, script: Script, player_info):
        script.power += self.power

    def on_script_replacement(self):
        self.power += 1
