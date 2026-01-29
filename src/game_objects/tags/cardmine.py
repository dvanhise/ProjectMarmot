from game_objects.tag import Tag


class CardMine(Tag):
    id = 'card-mine'
    icon = 'power'
    tooltip = 'Add {card} to draw pile when vector is captured.'
    count = 0
    card = ''

    part_of_vector = True
    remove_on_vector_change = False

    def __init__(self, *args, **kwargs):
        super().__init__(kwargs['count'])
        self.card = kwargs['card']

    def get_full_name(self):
        return f'{self.id}_{self.card}'

    def on_node_capture(self, node, vector):
        # TODO: Figure out how to add cards to player
        pass