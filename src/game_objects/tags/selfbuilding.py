from src.game_objects.tag import Tag


class SelfBuilding(Tag):
    id = 'self-building'
    name = 'Self-Building'
    icon = 'self_building'
    tooltip = 'Increase ward by {count} at end of turn.  Remove 1 stack.'

    def on_turn_end_node(self, vector, node):
        node.ward += self.count
        self.count -= 1

    # def on_vector_install(self, node, vector, player_info):
    #     node.tags.add_tag(vector.tags.pop(self))
