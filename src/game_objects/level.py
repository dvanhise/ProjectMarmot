

class Level:
    def __init__(self, definition):
        self.pattern = definition['pattern']
        self.planned_action = None
        self.hp = definition['hp']
        self.edge_difficulty = definition.get('edge_difficulty', 1)
        self.network_width = definition['network_width']
        self.network_height = definition['network_height']
        self.portrait = 'avatar2'  # FIXME
        self.health = 5

        self.nodes = {node['id']: Node(**node) for node in definition['nodes']}

        for e in definition['edges']:
            edge = Edge(self.nodes[e['left_id']], self.nodes[e['right_id']], e.get('difficulty', self.edge_difficulty))
            self.nodes[e['left_id']].right.append(edge)
            self.nodes[e['right_id']].left.append(edge)

    def get_source(self, owner):
        for node in self.nodes.values():
            if node.owner == owner and node.source:
                return node

        return None


class Node:
    def __init__(self, *args, **kwargs):
        self.id = kwargs['id']
        self.position = kwargs['position']
        self.ward = kwargs.get('ward', 0)
        self.vector = kwargs.get('vector', None)
        self.owner = kwargs.get('owner', 'NEUTRAL')
        self.name = kwargs.get('name')
        self.source = kwargs.get('source', False)
        self.left = []
        self.right = []

    def apply_ward(self):
        pass

    def apply_vector(self):
        pass


class Edge:
    def __init__(self, left: Node, right: Node, difficulty, owner='NEUTRAL'):
        self.left = left
        self.right = right
        self.difficulty = difficulty
        self.owner = owner
