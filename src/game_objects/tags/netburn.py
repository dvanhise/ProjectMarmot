from game_objects.tag import Tag


class NetBurn(Tag):
    id = 'net-burn'
    icon = 'burn'
    tooltip = 'Reduce ward by {count} at end of turn.'

    def on_turn_end_node(self, node):
        node.ward = max(0, node.ward - self.count)
        if node.ward == 0:
            node.vector = None

    def after_failed_script_node_encounter(self, script, node):
        node.tags.add_tag(script.tags.pop(self))