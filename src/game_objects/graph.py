from game_objects.vector import Vector


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

    def apply_ward(self, ward_value=0, ward_other=None):
        self.ward = max(self.ward, ward_value)
        # TODO: Alternate ward effects

    def install_vector(self, vector: Vector):
        self.vector = vector
        self.apply_ward(vector.default_ward)


class Edge:
    def __init__(self, left: Node, right: Node, difficulty, owner='NEUTRAL'):
        self.left = left
        self.right = right
        self.difficulty = difficulty
        self.owner = owner
