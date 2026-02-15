from src.game_objects.tag import Tag
from src.utils.action_queue import get_aq


class CardMine(Tag):
    id = 'card-mine'
    name = 'Card Mine'
    icon = 'power'
    tooltip = 'Add {count} copy of {card} to draw pile when node is captured.'
    card = ''

    def __init__(self, *args, **kwargs):
        super().__init__(kwargs['count'])
        self.card = kwargs['card']

    def get_full_name(self):
        return f'{self.id}{self.count}-{self.card}'

    def on_node_captured_as_node(self, script, node):
        get_aq().queue_action('add_card', self.card, 'draw')

    def on_node_captured_as_vector(self, script, node):
        get_aq().queue_action('add_card', self.card, 'draw')

    def on_vector_install(self, node, vector, player_info):
        # Move the tag to the node when the vector is installed
        node.tags.add_tag(vector.tags.pop(self))
