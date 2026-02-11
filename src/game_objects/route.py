import logging
import copy
from src.game_objects.graph import Node, Edge


class Route:
    def __init__(self, source_node, owner):
        self.owner = owner
        self.node_path = []
        self.edge_path = []

        self.node_path.append(source_node)

    def get_next_node_options(self) -> list[Node]:
        if self.owner == 'PLAYER':
            return [edge.right for edge in self.node_path[-1].right]
        elif self.owner == 'ENEMY':
            return [edge.left for edge in self.node_path[-1].left]
        else:
            raise ValueError('No paths found.')

    def get_next_edge_options(self) -> list[Edge]:
        if self.owner == 'PLAYER':
            return self.node_path[-1].right
        elif self.owner == 'ENEMY':
            return self.node_path[-1].left
        else:
            raise ValueError('No paths found.')

    def choose_next_node(self, node: Node):
        if node not in self.get_next_node_options():
            raise ValueError('Invalid node')

        self.node_path.append(node)
        self.edge_path.append(get_connecting_edge(self.node_path[-2], self.node_path[-1]))

    def choose_next_node_from_route(self, route: 'Route'):
        next_node = None
        for ndx, node in enumerate(route.node_path):
            if node == self.node_path[-1]:
                next_node = route.node_path[ndx+1]
                break

        if not next_node or next_node not in self.get_next_node_options():
            raise ValueError('Invalid node')

        self.node_path.append(next_node)
        self.edge_path.append(get_connecting_edge(self.node_path[-2], self.node_path[-1]))

    def is_path_complete(self):
        return len(self.node_path) > 1 and self.node_path[0].source and self.node_path[-1].source

    def create_copy(self):
        # copy.copy() and copy.deepcopy() over the whole object had unintended side effects
        route_copy = Route(None, self.owner)
        route_copy.node_path = copy.copy(self.node_path)
        route_copy.edge_path = copy.copy(self.edge_path)
        return route_copy


# Given two nodes, find the edge that connects them
def get_connecting_edge(node1: Node, node2: Node):
    for edge in node1.right:
        if edge in node2.left:
            return edge

    for edge in node1.left:
        if edge in node2.right:
            return edge

    return None