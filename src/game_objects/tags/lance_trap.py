from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class LanceTrap(Tag):
    id = 'lance-trap'
    name = 'Lance Trap'
    icon = 'card_mine'
    tooltip = "Add {count} copy of Lance (0-cost Payload, 6 Power, delete when executed) to the player's draw pile when node is captured."

    def on_node_capture_as_node(self, script, node):
        if script.owner == 'ENEMY':
            get_aq().queue_action('add_card', 'lance', 'draw')
        node.tags.remove(self)

    def on_node_capture_as_vector(self, script, node):
        if script.owner == 'ENEMY':
            get_aq().queue_action('add_card', 'lance', 'draw')
        node.vector.tags.remove(self)
