from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class EnergyDrain(Tag):
    id = 'energy-drain'
    name = 'Energy Drain'
    icon = 'tag_placeholder'
    tooltip = 'Gain {count} energy when capturing a node.'

    def on_node_capture_as_script(self, script, node):
        get_aq().queue_action('change_energy', self.count)
