from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class Bandwidth(Tag):
    id = 'bandwidth'
    name = 'Bandwidth'
    icon = 'power'
    tooltip = 'When a node is captured, gain {count} energy.'

    def on_node_captured_as_script(self, script, node):
        # FIXME: This needs to either check player tags or be applied to script
        get_aq().queue_action('change_energy', self.count)
