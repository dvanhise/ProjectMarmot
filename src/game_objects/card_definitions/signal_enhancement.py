from game_objects.script import Script
from game_objects.card_type import CardType
from game_objects.card import Card
from game_objects.tags.tag_multiplier import TagMultiplier


class SignalEnhancement(Card):
    id = 'signal-enhancement'
    name = 'Signal Enhancement'
    type = CardType.SCRIPT_MOD
    rarity = 'intermediate'
    image_id = 'mod',
    cost = 2
    description = ['Double positive tags', 'on each friendly node', 'and vector encountered']

    def on_script_activation(self, script: Script, player_info):
        script.tags.add_tag(TagMultiplier(2))
