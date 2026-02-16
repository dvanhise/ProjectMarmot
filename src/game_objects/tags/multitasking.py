from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class Multitasking(Tag):
    id = 'multitasking'
    name = 'Multitasking'
    icon = 'tag_placeholder'
    tooltip = 'When executing a script, draw {count} card.'

    def on_script_creation(self, script):
        if script.owner == 'PLAYER':
            get_aq().queue_action('draw_cards', self.count)
