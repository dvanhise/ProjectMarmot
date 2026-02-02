from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card


class BattleAxe(Card):
    id = 'battleaxe'
    name = 'Battle-axe'
    type = CardType.SCRIPT_PAYLOAD
    rarity = 'intermediate'
    image_id = 'payload',
    cost = 1
    description = ['1 power per card', 'in hand when executed']

    def on_script_activation(self, script: Script, player_info):
        script.power += player_info['cards_in_hand']
