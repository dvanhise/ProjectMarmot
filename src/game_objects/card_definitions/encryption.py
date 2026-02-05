from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card


class Encryption(Card):
    id = 'encryption'
    name = 'Encryption'
    type = CardType.SCRIPT_MOD
    rarity = 'simple'
    image_id = 'encryption'
    cost = 1
    description = ['Reduce script', 'edge penalty by 1']

    def on_script_activation(self, script: Script, player_info):
        script.edge_difficulty_reduction += 1
