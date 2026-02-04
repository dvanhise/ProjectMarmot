from game_objects.tag import Tag


class SelfBuilding(Tag):
    id = 'self-building'
    name = 'Self-Building'
    icon = 'heal'
    tooltip = 'Increase ward by {count} at end of turn.'

    def on_turn_end_vector(self, vector, node):
        node.ward += self.count
