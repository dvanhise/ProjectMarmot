from src.game_objects.card_type import CardType


class Card:
    name = 'default-name'
    id = ''
    cost = 0
    type = CardType.NULL
    description = 'Default description'
    tooltips = []
    rarity = 'simple'
    image_id = 'default'
    vector = None
    ward = 0
    power = 0
    delete_on_execution = False
    delete_on_play = False

    def get_description(self):
        return [line.format(ward=self.ward, power=self.power) for line in self.description]

    def on_play(self):
        pass

    def on_script_activation(self, script, player_info):
        pass

    def on_ward_install(self, node):
        pass

    def on_script_replacement(self):
        # When a script card replace another card in the script builder
        pass
