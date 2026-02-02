from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card


class ModularPolearm(Card):
    id = 'modulear-polearm'
    name = 'Modulear Polarm'
    type = CardType.SCRIPT_PAYLOAD
    rarity = 'intermediate'
    image_id = 'payload',
    cost = 1
    power = 6
    description = ['{power} power,', 'increase power by 2', 'when replacing a', 'script payload']

    def on_script_activation(self, script: Script, player_info):
        script.power += self.power

    def on_script_replacement(self):
        self.power += 2
