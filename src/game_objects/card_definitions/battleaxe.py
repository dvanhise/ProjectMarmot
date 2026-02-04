from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.power import Power


class BattleAxe(Card):
    id = 'battleaxe'
    name = 'Battle-axe'
    type = CardType.SCRIPT_PAYLOAD
    rarity = 'intermediate'
    image_id = 'payload',
    cost = 1
    description = ['1 Power per card', 'in hand when executed']
    tooltips = [Power]

    def on_script_activation(self, script: Script, player_info):
        script.power += player_info['cards_in_hand']
