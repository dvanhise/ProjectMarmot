from src.game_objects.tag import Tag
from src.game_objects.tags.boost import Boost


class BoostLoss(Tag):
    id = 'boost-loss'
    name = 'Boost Loss'
    icon = 'boost_loss'
    tooltip = 'On turn end, reduce boost by {count}.'
    count = 0
    positive = False

    def on_turn_end_node(self, vector, node):
        boost_tag = vector.tags.find_tag(Boost)
        if boost_tag:
            boost_tag.count -= 1

        if boost_tag.count <= 0:
            self.count = 0
