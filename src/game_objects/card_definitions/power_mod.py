from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card


class PowerMod(Card):
    id = 'power-mod'
    name = 'Power Mod'
    type = CardType.SCRIPT_MOD
    rarity = 'simple'
    image_id = 'mod',
    cost = 1
    description = ['+3 Power']

    def on_script_activation(self, script: Script, player_info):
        script.power += 3
