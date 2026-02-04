from game_objects.vector import Vector
from game_objects.card import Card
from game_objects.tag import TagManager


class Node:
    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.position = kwargs['position']
        self.ward = kwargs.get('ward', 0)
        self.vector = kwargs.get('vector', None)
        self.owner = kwargs.get('owner', 'NEUTRAL')
        self.name = kwargs.get('name')
        self.source = kwargs.get('source', False)
        self.health = kwargs.get('health', 1)
        self.left = []
        self.right = []
        self.tags = TagManager()
        for tag in kwargs.get('tags', []):
            self.tags.add_tag(tag)

    def apply_ward_from_card(self, card: Card):
        if card.ward:
            self.apply_ward(card.ward)

    def apply_ward(self, ward_value):
        self.ward = max(self.ward, ward_value)

    def install_vector(self, vector: Vector):
        self.vector = vector
        self.apply_ward(vector.default_ward)


class Edge:
    def __init__(self, left: Node, right: Node, difficulty, owner):
        self.left = left
        self.right = right
        self.difficulty = difficulty
        self.owner = owner
