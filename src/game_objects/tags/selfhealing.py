from game_objects.tag import Tag


class SelfHealing(Tag):
    id = 'self-healing'
    icon = 'heal'
    tooltip = 'Increase ward by {count} at end of turn.'
    count = 0

    def on_turn_end_vector(self, vector, node):
        node.ward += self.count
