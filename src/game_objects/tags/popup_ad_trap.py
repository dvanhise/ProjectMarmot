from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class PopupAdTrap(Tag):
    id = 'popup-ad-trap'
    name = 'Popup-Ad Trap'
    icon = 'card_mine'
    tooltip = "Add {count} copy of Popup-Ad (1-cost Utility, delete when played) to the player's draw pile when node is captured."

    def on_node_capture_as_node(self, script, node):
        if script.owner == 'PLAYER':
            get_aq().queue_action('add_card', 'popup-ad', 'draw')
        node.tags.remove(self)

    def on_node_capture_as_vector(self, script, node):
        if script.owner == 'PLAYER':
            get_aq().queue_action('add_card', 'popup-ad', 'draw')
        node.vector.tags.remove(self)
