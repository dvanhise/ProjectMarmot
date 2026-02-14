from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class Multitasking(Tag):
    id = 'multitasking'
    name = 'Multitasking'
    icon = 'power'
    tooltip = 'When executing a script, draw {count} card{"s" if count > 1 else ""}.'

    def on_script_creation(self, script):
        get_aq().queue_action('draw_cards', self.count)
