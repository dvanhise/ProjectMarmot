from src.game_objects.tag import Tag


class WardBuilder(Tag):
    id = 'ward-builder'
    name = 'Ward Builder'
    icon = 'tag_placeholder'
    tooltip = 'Applies {count} ward to each friendly node encountered.'
    count = 0

    def on_friendly_node_encounter_as_script(self, script, node):
        node.apply_ward(self.count)

    def on_node_capture_as_script(self, script, node):
        node.apply_ward(self.count)