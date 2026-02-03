from game_objects.tag import Tag
from utils.action_queue import get_aq


class Bandwidth(Tag):
    id = 'bandwidth'
    icon = 'power'
    tooltip = 'When a friendly node is captured, gain {count} energy.'

    def on_node_captured(self, node):
        get_aq().queue_action('change_energy', self.count)
