from src.game_objects.tag import Tag


class Boost(Tag):
    id = 'boost'
    name = 'Boost'
    icon = 'boost'
    tooltip = 'Increase script power by {count}.  Remove 1 stack when used.'
    count = 0

    def on_friendly_node_encounter_as_vector(self, script, node):
        script.power += self.count
        self.count -= 1