from game_objects.tags.fortify import Fortify
from game_objects.tags.surge import Surge
from game_objects.vector import Vector
from game_objects.tags.boost import Boost
from game_objects.tags.netburn import NetBurn
from utils.router import PathType

"""
     0   1   2   3   4
0           [4]
1       [2]     [7]
2   [1p]    [5]     [9e]
3       [3]     [8]
4           [6]
"""


definition = {
    'edge_difficulty': 2,
    'network_width': 5,
    'network_height': 5,
    'portrait': 'placeholder',
    'health': 5,
    'nodes': [
        {
            'id': 1,
            'position': (0, 2),
            'owner': 'PLAYER',
            'source': True
        },
        {
            'id': 2,
            'position': (1, 1)
        },
        {
            'id': 3,
            'position': (1, 3)
        },
        {
            'id': 4,
            'position': (2, 0)
        },
        {
            'id': 5,
            'position': (2, 2),
            'tags': [NetBurn(1)],
            'owner': 'ENEMY'
        },
        {
            'id': 6,
            'position': (2, 4)
        },
        {
            'id': 7,
            'position': (3, 1),
            'owner': 'ENEMY'
        },
        {
            'id': 8,
            'name': 'Database',
            'position': (3, 3),
            'owner': 'ENEMY'
        },
        {
            'id': 9,
            'position': (4, 2),
            'owner': 'ENEMY',
            'source': True
        }
    ],
    'edges': [
        {
            'left_id': 1,
            'right_id': 2
        },
        {
            'left_id': 1,
            'right_id': 3
        },
        {
            'left_id': 2,
            'right_id': 4
        },
        {
            'left_id': 2,
            'right_id': 5
        },
        {
            'left_id': 3,
            'right_id': 5
        },
        {
            'left_id': 3,
            'right_id': 6
        },
        {
            'left_id': 4,
            'right_id': 7
        },
        {
            'left_id': 5,
            'right_id': 7
        },
        {
            'left_id': 5,
            'right_id': 8
        },
        {
            'left_id': 6,
            'right_id': 8
        },
        {
            'left_id': 7,
            'right_id': 9
        },
        {
            'left_id': 8,
            'right_id': 9
        }
    ],
    'pattern': [
        {
            'pattern_id': 1,
            'start': True,
            'power': 3,
            'vectors': [
                Vector(name='Fire', default_ward=4, tags=[Boost(1), NetBurn(1)]),
                Vector(name='Fire', default_ward=4, tags=[Boost(1), NetBurn(1)]),
                Vector(name='Fire', default_ward=4, tags=[Boost(1), NetBurn(1)])
            ],
            'pathing': PathType.RANDOM,
            'next': 2
        },
        {
            'pattern_id': 2,
            'power': 6,
            'tags': [NetBurn(2)],
            'pathing': PathType.CLOSEST_ENEMY_NODE,
            'next': 3
        },
        {
            'pattern_id': 3,
            'power': 4,
            'tags': [Surge(1)],
            'vectors': [Vector(name='Smoke', default_ward=6, tags=[Boost(3), Fortify(1), NetBurn(1)])],
            'pathing': PathType.TAKE_OPPONENT_NODES,
            'next': 1
        }
    ]
}
