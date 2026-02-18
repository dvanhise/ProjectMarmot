from src.game_objects.card_type import CardType


class Card:
    name = 'default-name'
    id = ''
    cost = 0
    type = CardType.NULL
    description = ['Default description']
    tooltips = []  # Helpful tooltips that reference tags
    rarity = 'simple'
    image_id = 'default'
    vector = None
    ward = 0
    power = 0
    other1 = 0  # Generic other attributes that specific cards can use
    other2 = 0
    other3 = 0
    delete_on_execution = False
    delete_on_play = False

    def get_description(self):
        return [
            line.format(ward=self.ward,
                        power=self.power,
                        other1=self.other1,
                        other2=self.other2,
                        other3=self.other3)
            for line in self.description
        ]

    def on_play(self):
        pass

    def on_script_activation(self, script, player_info):
        pass

    def on_ward_install(self, node):
        pass

    def on_script_overwrite(self):
        # When a script card replaces another card in the script builder
        pass

    def on_script_overwritten(self):
        # When a script card is replaced by another card in the script builder
        pass