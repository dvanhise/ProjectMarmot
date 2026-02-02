from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card


class Shiv(Card):
    id = 'shiv'
    name = 'Shiv'
    type = CardType.SCRIPT_PAYLOAD
    rarity = 'simple'
    image_id = 'payload',
    cost = 0
    power = 2
    description = ['{power} power']

    def on_script_activation(self, script: Script, player_info):
        script.power += self.power
