from game_objects.tag import Tag
from game_objects.tags.boost import Boost


class BoostLoss(Tag):
    id = 'boost-loss'
    icon = 'power'
    tooltip = 'On turn end, reduce boost by {count}.'
    count = 0

    def on_turn_end_vector(self, vector, node):
        boost_tag = vector.tags.find_tag(Boost)
        if boost_tag:
            boost_tag.count -= 1
