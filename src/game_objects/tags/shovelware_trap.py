from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class ShovelwareTrap(Tag):
    id = 'shovelware-trap'
    name = 'Shovelware Trap'
    icon = 'card_mine'
    tooltip = "Add {count} copy of Shovelware (0-cost Script mod, delete when executed) to the player's draw pile when node is captured."

    def on_node_capture_as_node(self, script, node):
        if script.owner == 'PLAYER':
            get_aq().queue_action('add_card', 'shovelware', 'draw')
        node.tags.remove(self)

    def on_node_capture_as_vector(self, script, node):
        if script.owner == 'PLAYER':
            get_aq().queue_action('add_card', 'shovelware', 'draw')
        node.vector.tags.remove(self)
