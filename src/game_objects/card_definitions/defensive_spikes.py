from src.game_objects.card_type import CardType
from src.game_objects.card import Card
from src.game_objects.tags.fortify import Fortify


class DefensiveSpikes(Card):
    id = 'defensive-spikes'
    name = 'Defensive Spikes'
    type = CardType.WARD
    rarity = 'intermediate'
    tooltips = [Fortify]
    image_id = 'defensive-spikes'
    cost = 3
    description = ['Apply Fortify {other1}.', 'Reduce fortify amount', 'by 1 this encounter.']
    other1 = 3  # Fortify value

    def on_ward_install(self, node):
        if self.other1 >= 1:
            node.tags.add_tag(Fortify(self.other1))
            self.other1 -=1
