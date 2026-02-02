from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card


class Spike(Card):
    id = 'spike'
    name = 'Spike'
    type = CardType.SCRIPT_PAYLOAD
    rarity = 'built-in'
    image_id = 'payload',
    cost = 1
    power = 2
    description = ['{power} power']

    def on_script_activation(self, script: Script, player_info):
        script.power += self.power
