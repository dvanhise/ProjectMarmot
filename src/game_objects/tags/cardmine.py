from game_objects.tag import Tag
from utils.action_queue import get_aq


class CardMine(Tag):
    id = 'card-mine'
    name = 'Card Mine'
    icon = 'power'
    tooltip = 'Add {count} copy of {card} to draw pile when vector is captured.'
    card = ''

    part_of_vector = True
    remove_on_vector_change = False

    def __init__(self, *args, **kwargs):
        super().__init__(kwargs['count'])
        self.card = kwargs['card']

    def get_full_name(self):
        return f'{self.id}_{self.card}'

    def on_node_captured(self, node):
        get_aq().queue_action('add_card', self.card, 'draw')
