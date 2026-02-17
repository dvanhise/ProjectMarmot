from src.game_objects.tag import Tag


class Fortify(Tag):
    id = 'fortify'
    name = 'Fortify'
    icon = 'fortify'
    tooltip = 'Automatically repels attacking script.  Remove 1 stack when attacked.'

    def on_vector_install_as_vector(self, script, node, vector, player_info):
        # Move the tag to the node when the vector is installed
        vector.tags.remove(self)
        node.tags.add_tag(self)

    def before_node_encounter_as_node(self, script, node):
        if script.owner != node.owner:
            script.power = -1
            self.count -= 1
