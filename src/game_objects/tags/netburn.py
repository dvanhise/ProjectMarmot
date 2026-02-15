from src.game_objects.tag import Tag


class NetBurn(Tag):
    id = 'net-burn'
    name = 'Netburn'
    icon = 'burn'
    tooltip = 'Reduce ward by {count} at end of turn.  Half of value spreads via scripts.'
    positive = False

    def on_turn_end_node(self, vector, node):
        node.ward = max(0, node.ward - self.count)

    def on_vector_install(self, node, vector, player_info):
        if self == vector.tags.find_tag(NetBurn):
            vector.tags.remove(self)
            node.tags.add_tag(self)

    def on_failed_node_encounter_as_script(self, script, node):
        script.tags.remove(self)
        node.tags.add_tag(self)

    def on_friendly_node_encounter_as_node(self, script, node):
        if self.count > 1:
            script.tags.add_tag(NetBurn(self.count // 2))

    def on_node_captured_as_node(self, script, node):
        if self.count > 1:
            script.tags.add_tag(NetBurn(self.count // 2))