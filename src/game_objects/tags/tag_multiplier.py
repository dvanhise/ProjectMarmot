from src.game_objects.tag import Tag


class TagMultiplier(Tag):
    id = 'tag-multiplier'
    name = 'Tag Multiplier'
    icon = 'tag_placeholder'
    tooltip = 'Increases all friendly node and vector tags by {count}x.'

    def on_friendly_node_encounter_as_script(self, script, node):
        for tag in node.tags:
            if tag.positive:
                tag.count *= self.count

        if node.vector:
            for tag in node.vector.tags:
                if tag.positive:
                    tag.count *= self.count
