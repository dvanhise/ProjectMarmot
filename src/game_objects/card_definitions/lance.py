from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.power import Power


class Lance(Card):
    id = 'lance'
    name = 'Lance'
    type = CardType.SCRIPT_PAYLOAD
    rarity = 'special'
    tooltips = [Power]
    image_id = 'payload'
    cost = 0
    power = 6
    description = ['{power} Power', 'Delete when executed']
    delete_on_execution = True

    def on_script_activation(self, script: Script, player_info):
        script.power += self.power
