import logging
import random
from game_objects.level import Level, Node, get_connecting_edge
from game_objects.script import Script


class Route:
    def __init__(self, level: Level, owner, script: Script):
        self.level = level
        self.owner = owner
        self.script = script
        self.node_path = []
        self.edge_path = []

        # Find source node
        for node in self.level.nodes:
            if node.owner == self.owner and node.source:
                self.node_path.append(node)
                break

        if not len(self.node_path):
            logging.critical(f'Failed to found source node with owner "{self.owner}"')
            raise ValueError('No source node found.')

    def get_next_node_options(self) -> list[Node]:
        if self.owner == 'PLAYER':
            return [edge.right for edge in self.node_path[-1].right]
        elif self.owner == 'ENEMY':
            return [edge.left for edge in self.node_path[-1].left]
        else:
            raise ValueError('No paths found.')

    def choose_next_node(self, node: Node):
        if node not in self.get_next_node_options():
            raise ValueError('Invalid node')
        
        self.node_path.append(node)
        self.edge_path.append(get_connecting_edge(self.node_path[-2], self.node_path[-1]))

    def is_path_complete(self):
        return len(self.node_path) > 1 and self.node_path[0].source and self.node_path[-1].source

    def generate_path(self, pathing_type='RANDOM'):
        if pathing_type == 'RANDOM':
            while not self.is_path_complete():
                self.choose_next_node(random.choice(self.get_next_node_options()))

        else:
            raise ValueError(f'Pathing type "{pathing_type}" not implemented yet')


    # TODO: Methods for undoing choices or skipping nodes