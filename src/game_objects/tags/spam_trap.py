from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class SpamTrap(Tag):
    id = 'spam-trap'
    name = 'Spam Trap'
    icon = 'card_mine'
    tooltip = "Add {count} copy of Spam (Unplayable) to the player's discard pile when node is captured."

    def on_node_capture_as_node(self, script, node):
        if script.owner == 'PLAYER':
            get_aq().queue_action('add_card', 'spam', 'discard')
        node.tags.remove(self)

    def on_node_capture_as_vector(self, script, node):
        if script.owner == 'PLAYER':
            get_aq().queue_action('add_card', 'spam', 'discard')
        node.vector.tags.remove(self)
