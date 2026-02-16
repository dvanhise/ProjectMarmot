import random
from src.game_objects.tags.fortify import Fortify
from src.game_objects.vector import Vector
from src.game_objects.tags.boost import Boost
from src.game_objects.tags.enemy_surge import EnemySurge
from src.utils.router import PathType


"""
Small network with unbalanced edge difficulty

     0   1   2
0       [2]
1   [1p]    [4e]
2       [3]
"""


definition = {
    'edge_difficulty': 2,
    'network_width': 3,
    'network_height': 3,
    'portrait': 'placeholder',
    'health': 6,
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
            'position': (1, 2)
        },
        {
            'id': 4,
            'position': (2, 1),
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
            'right_id': 3,
            'difficulty': 4
        },
        {
            'left_id': 2,
            'right_id': 4,
            'difficulty': 4
        },
        {
            'left_id': 3,
            'right_id': 4
        }
    ],
    'pattern': [
        {
            'pattern_id': 1,
            'start': True,
            'power': 4,
            'vectors': [Vector(name='Amp', default_ward=1, tags=[Boost(2)])],
            'pathing': PathType.TAKE_NODES,
            'next': lambda prev: random.choice([2,3])
        },
        {
            'pattern_id': 2,
            'start': True,
            'power': 5,
            'vectors': [Vector(name='Amp', tags=[Boost(2)])],
            'pathing': PathType.ATTACK_OPPONENT_SOURCE,
            'next': 3
        },
        {
            'pattern_id': 3,
            'power': 3,
            'self_tags': [EnemySurge(1)],
            'vectors': [Vector(name='Stop', tags=[Boost(1), Fortify(1)])],
            'pathing': PathType.RANDOM,
            'next': 1
        }
    ]
}