from src.game_objects.tag import Tag


class TagMultiplier(Tag):
    id = 'tag-multiplier'
    name = 'Tag Multiplier'
    icon = 'power'
    tooltip = 'Increases all friendly node and vector tags by {count+1}x.'

    def on_friendly_script_node_encounter(self, script, node):
        for tag in node.tags:
            tag.count *= (self.count + 1)

        if node.vector:
            for tag in node.vector.tags:
                tag.count *= (self.count + 1)
