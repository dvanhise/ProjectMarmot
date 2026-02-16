import copy
from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class Bandwidth(Tag):
    id = 'bandwidth'
    name = 'Bandwidth'
    icon = 'tag_placeholder'
    tooltip = 'When a friendly node is captured, gain {count} energy.'

    # Add the player tag to enemy scripts
    def on_script_creation(self, script):
        # FIXME: This doesn't work because the player tags don't get triggered for enemy script creation
        if script.owner == 'ENEMY':
            script.tags.add_tag(copy.deepcopy(self))

    def on_node_capture_as_script(self, script, node):
        get_aq().queue_action('change_energy', self.count)
