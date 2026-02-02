from game_objects.tag import Tag


class WardBuilder(Tag):
    id = 'ward-builder'
    icon = 'power'
    tooltip = 'Applies {count} ward to each friendly node encountered.'
    count = 0

    def on_friendly_script_node_encounter(self, script, node):
        node.apply_ward(self.count)