from game_objects.tag import Tag


class Fortify(Tag):
    id = 'fortify'
    name = 'Fortify'
    icon = 'heal'
    tooltip = 'Repels attacking script.  Remove 1 stack when attacked.'

    def before_script_node_encounter(self, script, node):
        script.power = -1
        self.count -= 1
