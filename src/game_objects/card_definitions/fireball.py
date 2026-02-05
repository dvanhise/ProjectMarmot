from game_objects.script import Script
from game_objects.tags.netburn import NetBurn
from game_objects.card_type import CardType
from game_objects.card import Card


class Fireball(Card):
    id = 'fireball'
    name = 'Fireball'
    type = CardType.SCRIPT_MOD
    rarity = 'simple'
    tooltips = [NetBurn]
    image_id = 'fireball'
    cost = 0
    description = ['Add Netburn to script']

    def on_script_activation(self, script: Script, player_info):
        script.tags.add_tag(NetBurn(2))
