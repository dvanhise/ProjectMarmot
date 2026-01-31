import copy
import logging
import random
from game_objects.graph import Node, Edge
from game_objects.script import Script
from game_objects.tags.boost import Boost


class Route:
    def __init__(self, source_node, owner):
        self.owner = owner
        self.node_path = []
        self.edge_path = []

        self.node_path.append(source_node)

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

        # TODO: Methods for undoing choices or skipping nodes

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

    def generate_path(self, pathing_type: str, script: Script):
        all_paths = self.get_all_paths()
        stats = [route.get_expected_stats() for route in all_paths]

        if pathing_type == 'RANDOM':
            while not self.is_path_complete():
                self.choose_next_node(random.choice(self.get_next_node_options()))

        elif pathing_type == 'CLOSEST_ENEMY_NODE':
            # Target closest enemy node
            pass

        elif pathing_type == 'MAX_BOOST':
            # Maximize vector boost
            pass

        elif pathing_type == 'ATTACK_ENEMY_SOURCE':
            # Highest power attack on enemy source
            pass

        elif pathing_type == 'TAKE_ENEMY_NODES':
            # Path that defeats the most enemy-controlled nodes
            pass

        else:
            raise ValueError(f'Pathing type "{pathing_type}" not implemented.')

    def get_expected_stats(self, script):
        # Evaluate boost, ward, and edge penalty only
        stats = {
            'nodes_taken': 0,
            'enemy_nodes_taken': 0,
            'distance_at_first_enemy_node': 0,
            'nodes_touched': 0,
            'boost_gained': 0,
            'power_at_enemy_source': 0
        }

        power = script.power
        ndx = 0
        node_check = True
        while power >= 0 and ndx < len(self.node_path):
            if node_check:
                node = self.node_path[ndx]
                if node.owner == self.owner:
                    stats['nodes_touched'] += 1
                    if node.vector:
                        for tag in [t for t in node.vector.tags if type(t) is Boost]:
                            stats['boost_gained'] += tag.count
                            power += tag.count
                else:
                    if node.owner not in ['NEUTRAL', self.owner] and stats['distance_at_first_enemy_node'] == 0:
                        stats['distance_at_first_enemy_node'] = ndx

                    power -= node.ward
                    if node.owner == 'NEUTRAL' and power >= 0:
                        stats['nodes_taken'] += 1
                        stats['nodes_touched'] += 1
                    elif power >= 0:
                        stats['nodes_taken'] += 1
                        stats['enemy_nodes_taken'] += 1
                        stats['nodes_touched'] += 1
                        if node.source:
                            stats['power_at_enemy_source'] = power

            if not node_check:
                edge = self.edge_path[ndx]
                if edge.owner != self.owner:
                    power -= edge.difficulty

                ndx += 1

            node_check = not node_check

        return stats

    def get_all_paths(self):
        routes = [Route(self.node_path[0], self.owner)]
        next_routes = []
        complete_routes = []
        while len(routes):
            for r in routes:
                for node in r.get_next_node_options():
                    new_route = copy.deepcopy(r)
                    new_route.choose_next_node(node)

                    if new_route.is_path_complete():
                        complete_routes.append(new_route)
                    else:
                        next_routes.append(new_route)

            routes = next_routes
            next_routes = []

        return complete_routes


# Given two nodes, find the edge that connects them
def get_connecting_edge(node1: Node, node2: Node):
    for edge in node1.right:
        if edge in node2.left:
            return edge

    for edge in node1.left:
        if edge in node2.right:
            return edge

    return None