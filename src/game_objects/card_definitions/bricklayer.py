from game_objects.script import Script
from game_objects.tags.ward_builder import WardBuilder
from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.ward import Ward



class Bricklayer(Card):
    id = 'bricklayer'
    name = 'Bricklayer'
    type = CardType.SCRIPT_MOD
    rarity = 'elite'
    image_id = 'bricklayer'
    tooltips = [Ward]
    cost = 1
    description = ['Apply 2 ward to', 'each node encountered']

    def on_script_activation(self, script: Script, player_info):
        script.tags.add_tag(WardBuilder(2))
