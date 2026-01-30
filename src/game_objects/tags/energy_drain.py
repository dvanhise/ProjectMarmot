from game_objects.tag import Tag
from utils.action_queue import get_aq


class EnergyDrain(Tag):
    id = 'energy-drain'
    icon = 'power'
    tooltip = 'Gain {count} energy when capturing a node.'
    count = 0

    def after_successful_script_node_encounter(self, script, node):
        get_aq().queue_action('change_energy', self.count)
