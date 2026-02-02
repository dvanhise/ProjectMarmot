from game_objects.tag import Tag


class Boost(Tag):
    id = 'boost'
    icon = 'power'
    tooltip = 'Increase script power by {count}.  Remove 1 stack when used.'
    count = 0

    part_of_vector = True
    remove_on_vector_change = False

    def get_full_name(self):
        return f'{self.id}{self.count}'

    def on_friendly_script_node_encounter(self, script, node):
        script.power += self.count
        self.count -= 1