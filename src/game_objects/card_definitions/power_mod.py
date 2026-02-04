from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.power import Power


class PowerMod(Card):
    id = 'power-mod'
    name = 'Power Mod'
    type = CardType.SCRIPT_MOD
    rarity = 'simple'
    tooltips = [Power]
    image_id = 'mod',
    cost = 1
    description = ['+3 Power']

    def on_script_activation(self, script: Script, player_info):
        script.power += 3
