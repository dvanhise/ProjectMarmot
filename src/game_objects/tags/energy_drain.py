from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class EnergyDrain(Tag):
    id = 'energy-drain'
    name = 'Energy Drain'
    icon = 'power'
    tooltip = 'Gain {count} energy when capturing a node.'

    def after_successful_script_node_encounter(self, script, node):
        get_aq().queue_action('change_energy', self.count)
