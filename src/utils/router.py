import random
import copy
import logging
from enum import StrEnum, auto
from src.game_objects.graph import Node
from src.game_objects.route import Route
from src.game_objects.script import Script
from src.game_objects.tags.boost import Boost


class PathType(StrEnum):
    RANDOM = auto()
    CLOSEST_ENEMY_NODE = auto()
    MAX_BOOST = auto()
    ATTACK_OPPONENT_SOURCE = auto()
    TAKE_OPPONENT_NODES = auto()


def generate_route(source_node: Node, script: Script):
    all_paths = get_all_paths(source_node, script.owner)
    stats = [get_expected_stats(route, script) for route in all_paths]

    if script.pathing == PathType.RANDOM:
        route = Route(source_node, script.owner)
        while not route.is_path_complete():
            route.choose_next_node(random.choice(route.get_next_node_options()))
        return route

    elif script.pathing == PathType.CLOSEST_ENEMY_NODE:
        max_stat = max([s['distance_at_first_enemy_node'] for s in stats])
        chosen_ndx = random.choice([ndx for ndx, s in enumerate(stats) if s['distance_at_first_enemy_node'] == max_stat])
        return all_paths[chosen_ndx]

    elif script.pathing == PathType.MAX_BOOST:
        max_stat = max([s['boost_gained'] for s in stats])
        chosen_ndx = random.choice([ndx for ndx, s in enumerate(stats) if s['boost_gained'] == max_stat])
        return all_paths[chosen_ndx]

    elif script.pathing == PathType.ATTACK_OPPONENT_SOURCE:
        max_stat = max([s['power_at_enemy_source'] for s in stats])
        chosen_ndx = random.choice([ndx for ndx, s in enumerate(stats) if s['power_at_enemy_source'] == max_stat])
        return all_paths[chosen_ndx]

    elif script.pathing == PathType.TAKE_OPPONENT_NODES:
        max_stat = max([s['enemy_nodes_taken'] for s in stats])
        chosen_ndx = random.choice([ndx for ndx, s in enumerate(stats) if s['enemy_nodes_taken'] == max_stat])
        return all_paths[chosen_ndx]

    else:
        raise ValueError(f'Pathing type "{script.pathing}" not implemented.')


def get_expected_stats(route, script):
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
    while power >= 0 and ndx < len(route.node_path):
        if node_check:
            node = route.node_path[ndx]
            if node.owner == route.owner:
                stats['nodes_touched'] += 1
                if node.vector:
                    boost_tag = node.vector.tags.find_tag(Boost)
                    if boost_tag:
                        stats['boost_gained'] += boost_tag.count
                        power += boost_tag.count
            else:
                if node.owner not in ['NEUTRAL', route.owner] and stats['distance_at_first_enemy_node'] == 0:
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
            if ndx < len(route.edge_path):
                edge = route.edge_path[ndx]
                if edge.owner != route.owner:
                    power -= edge.difficulty
            ndx += 1

        node_check = not node_check

    return stats


def get_all_paths(source_node, owner):
    routes = [Route(source_node, owner)]
    next_routes = []
    complete_routes = []
    while len(routes):
        for r in routes:
            for node in r.get_next_node_options():
                new_route = r.create_copy()
                new_route.choose_next_node(node)

                if new_route.is_path_complete():
                    complete_routes.append(new_route)
                else:
                    next_routes.append(new_route)

        routes = next_routes
        next_routes = []

    return complete_routes
