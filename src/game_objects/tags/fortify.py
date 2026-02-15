from src.game_objects.tag import Tag


class Fortify(Tag):
    id = 'fortify'
    name = 'Fortify'
    icon = 'heal'
    tooltip = 'Automatically repels attacking script.  Remove 1 stack when attacked.'

    def before_node_encounter_as_node(self, script, node):
        script.power = -1
        self.count -= 1
