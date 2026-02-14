from src.game_objects.card_type import CardType
from src.game_objects.card import Card
from src.game_objects.script import Script


class Shovelware(Card):
    id = 'shovelware'
    name = 'Shovelware'
    type = CardType.SCRIPT_MOD
    rarity = 'special'
    image_id = 'placeholder'
    cost = 0
    description = ['Delete when executed']
    delete_on_execution = True

    def on_script_activation(self, script: Script, player_info):
        script.power += 0
