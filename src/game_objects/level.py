

class Level:
    def __init__(self, nodes, edges, pattern, other):
        self.pattern = pattern
        self.edge_difficulty = other.get('edge_difficulty', 1)
        self.board_width = other['board_width']
        self.board_height = other['board_height']

        self.nodes = {node['id']: Node(**node) for node in nodes}

        for e in edges:
            edge = Edge(self.nodes[e['left_id']], self.nodes[e['right_id']], e.get('difficulty', self.edge_difficulty))
            self.nodes[e['left_id']].right.append(edge)
            self.nodes[e['right_id']].left.append(edge)


class Node:
    def __init__(self, *args, **kwargs):
        self.position = kwargs['position']
        self.ward = kwargs.get('ward', 0)
        self.vector = kwargs.get('vector', '')
        self.owner = kwargs.get('owner', 'NEUTRAL')
        self.name = kwargs.get('name')
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
