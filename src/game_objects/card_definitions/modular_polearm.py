from src.game_objects.script import Script
from src.game_objects.card_type import CardType
from src.game_objects.card import Card
from src.game_objects.tags.power import Power
from src.game_objects.tags.overwrite import Overwrite


class ModularPolearm(Card):
    id = 'modular-polearm'
    name = 'Modular Polearm'
    type = CardType.SCRIPT_PAYLOAD
    rarity = 'intermediate'
    tooltips = [Power, Overwrite]
    image_id = 'payload'
    cost = 1
    power = 3
    description = ['{power} Power.', 'When this card', 'overwrites another,', 'Increase power by 1', 'this encounter.']

    def on_script_activation(self, script: Script, player_info):
        script.power += self.power

    def on_script_overwrite(self):
        self.power += 1
