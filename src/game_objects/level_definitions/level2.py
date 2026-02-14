from src.game_objects.tags.boost import Boost
from src.game_objects.vector import Vector
from src.utils.router import PathType

"""
Lots of enemy starting nodes with high ward

     0      1       2       3       4       5
0          [2]     [4]     [6]     [8]
1   [1p]                                    [10e]
2          [3]     [5]     [7]     [9]
"""


definition = {
    'edge_difficulty': 2,
    'network_width': 6,
    'network_height': 3,
    'portrait': 'placeholder',
    'health': 3,
    'nodes': [
        {
            'id': 1,
            'position': (0, 1),
            'owner': 'PLAYER',
            'source': True
        },
        {
            'id': 2,
            'position': (1, 0)
        },
        {
            'id': 3,
            'position': (1, 2),
        },
        {
            'id': 4,
            'position': (2, 0)
        },
        {
            'id': 5,
            'position': (2, 2),
            'owner': 'ENEMY',
            'ward': 1
        },
        {
            'id': 6,
            'position': (3, 0),
            'owner': 'ENEMY',
            'ward': 1
        },
        {
            'id': 7,
            'position': (3, 2),
            'owner': 'ENEMY',
            'ward': 1
        },
        {
            'id': 8,
            'position': (4, 0),
            'owner': 'ENEMY',
            'ward': 1
        },
        {
            'id': 9,
            'position': (4, 2),
            'owner': 'ENEMY',
            'ward': 1
        },
        {
            'id': 10,
            'position': (5, 1),
            'owner': 'ENEMY',
            'source': True,
            'ward': 1
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
            'left_id': 3,
            'right_id': 5
        },
        {
            'left_id': 4,
            'right_id': 6
        },
        {
            'left_id': 5,
            'right_id': 7
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
            'right_id': 10
        },
        {
            'left_id': 9,
            'right_id': 10
        }
    ],
    'pattern': [
        {
            'pattern_id': 1,
            'start': True,
            'power': 2,
            'vectors': [Vector(name='Shield', default_ward=3, tags=[Boost(1)]), Vector(name='Spear', tags=[Boost(2)])],
            'pathing': PathType.RANDOM,
            'next': 2
        },
        {
            'pattern_id': 2,
            'power': 5,
            'pathing': PathType.ATTACK_OPPONENT_SOURCE,
            'next': 1
        }
    ]
}
