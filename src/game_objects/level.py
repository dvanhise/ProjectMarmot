import logging
from src.game_objects.graph import Node, Edge
from src.game_objects.tag import TagManager


class Level:
    def __init__(self, definition):
        self.edge_difficulty = definition.get('edge_difficulty', 1)
        self.network_width = definition['network_width']
        self.network_height = definition['network_height']
        self.portrait = definition['portrait']
        self.health = definition['health']
        self.tags = TagManager()

        self.nodes = {node['id']: Node(**node) for node in definition['nodes']}

        for e in definition['edges']:
            owner = 'NEUTRAL'
            if self.nodes[e['left_id']].owner == self.nodes[e['right_id']].owner:
                owner = self.nodes[e['left_id']].owner
            edge = Edge(self.nodes[e['left_id']], self.nodes[e['right_id']], e.get('difficulty', self.edge_difficulty), owner)
            self.nodes[e['left_id']].right.append(edge)
            self.nodes[e['right_id']].left.append(edge)


    def get_source(self, owner):
        for node in self.nodes.values():
            if node.owner == owner and node.source:
                return node
        raise ValueError(f'Source node for "{owner}" could not be found.')

    def remove_depleted_vectors(self):
        [node.check_vector_depletion() for node in self.nodes.values()]

    def check_win(self):
        return self.health <= 0
