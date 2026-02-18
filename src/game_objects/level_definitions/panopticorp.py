import random

from src.game_objects.vector import Vector
from src.game_objects.tags.boost import Boost
from src.game_objects.tags.enemy_surge import EnemySurge
from src.game_objects.tags.selfbuilding import SelfBuilding
from src.game_objects.tags.fortify import Fortify
from src.utils.router import PathType


"""
Large network with self-building and ward on vectors

     0   1   2   3   4
0       [2]     [7]
1           [5]
2  [1p] [3]     [8] [10e]
3           [6]
4       [4]     [9]
"""


definition = {
    'edge_difficulty': 2,
    'network_width': 5,
    'network_height': 5,
    'portrait': 'placeholder',
    'name': 'PanoptiCorp',
    'health': 4,
    'nodes': [
        {
            'id': 1,
            'position': (0, 2),
            'owner': 'PLAYER',
            'source': True
        },
        {
            'id': 2,
            'position': (1, 0)
        },
        {
            'id': 3,
            'position': (1, 2)
        },
        {
            'id': 4,
            'position': (1, 4)
        },
        {
            'id': 5,
            'position': (2, 1)
        },
        {
            'id': 6,
            'position': (2, 3)
        },
        {
            'id': 7,
            'position': (3, 0)
        },
        {
            'id': 8,
            'position': (3, 2),
            'tags': [SelfBuilding(2)],
            'owner': 'ENEMY'
        },
        {
            'id': 9,
            'position': (3, 4)
        },
        {
            'id': 10,
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
            'left_id': 1,
            'right_id': 4
        },
        {
            'left_id': 2,
            'right_id': 7
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
            'right_id': 8
        },
        {
            'left_id': 3,
            'right_id': 6
        },
        {
            'left_id': 4,
            'right_id': 6
        },
        {
            'left_id': 4,
            'right_id': 9
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
            'left_id': 6,
            'right_id': 9
        },
        {
            'left_id': 7,
            'right_id': 10
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
            'power': 4,
            'vectors': [
                Vector(name='Amp', tags=[Boost(1)]),
                Vector(name='++', default_ward=1, tags=[SelfBuilding(3), Fortify(1)])
            ],
            'pathing': PathType.TAKE_NODES,
            'next': 2
        },
        {
            'pattern_id': 2,
            'power': 6,
            'pathing': PathType.TAKE_OPPONENT_NODES,
            'next': 3
        },
        {
            'pattern_id': 3,
            'power': 4,
            'vectors': [
                Vector(name='Amp', tags=[Boost(2)]),
                Vector(name='++', default_ward=1, tags=[SelfBuilding(3)])
            ],
            'pathing': PathType.TAKE_NODES,
            'next': 4
        },
        {
            'pattern_id': 4,
            'power': 3,
            'self_tags': [EnemySurge(1)],
            'vectors': [Vector(name='Amp', tags=[Boost(2)])],
            'pathing': PathType.RANDOM,
            'next': lambda prev: random.choice([2,3])
        },
    ]
}