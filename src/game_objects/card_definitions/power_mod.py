from src.game_objects.script import Script
from src.game_objects.card_type import CardType
from src.game_objects.card import Card
from src.game_objects.tags.power import Power


class PowerMod(Card):
    id = 'power-mod'
    name = 'Power Mod'
    type = CardType.SCRIPT_MOD
    rarity = 'simple'
    tooltips = [Power]
    image_id = 'mod'
    cost = 1
    description = ['+2 Power']

    def on_script_activation(self, script: Script, player_info):
        script.power += 2
