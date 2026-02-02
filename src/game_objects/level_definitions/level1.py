from game_objects.vector import Vector
from game_objects.tags.boost import Boost
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
    'portrait': 'avatar2',
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
            'position': (2, 2)
        },
        {
            'id': 6,
            'position': (2, 4)
        },
        {
            'id': 7,
            'position': (3, 1)
        },
        {
            'id': 8,
            'name': 'Database',
            'position': (3, 3),
            'owner': 'ENEMY',
            'ward': 4,
            'vector': Vector(name='Amp', tags=[Boost(2)])
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
            'vector': Vector(name='Amp', default_ward=1, tags=[Boost(2)]),
            'pathing': PathType.RANDOM,
            'next': 2
        },
        {
            'pattern_id': 2,
            'power': 5,
            'pathing': PathType.TAKE_OPPONENT_NODES,
            'next': 1
        }
    ]
}
