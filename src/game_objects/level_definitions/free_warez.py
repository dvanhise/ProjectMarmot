import random

from src.game_objects.tags.boost import Boost
from src.game_objects.tags.enemy_surge import EnemySurge
from src.game_objects.tags.popup_ad_trap import PopupAdTrap
from src.game_objects.tags.shovelware_trap import ShovelwareTrap
from src.game_objects.tags.spam_trap import SpamTrap
from src.game_objects.vector import Vector
from src.utils.router import PathType

"""
Taking enemy vectors gives trash cards

     0      1       2       3       4       5
0          [2]     [4]     [6]     [8]
1   [1p]        x       x       x          [10e]
2          [3]     [5]     [7]     [9]
"""

definition = {
    'edge_difficulty': 2,
    'network_width': 6,
    'network_height': 3,
    'portrait': 'placeholder',
    'name': 'free_warez.ru',
    'health': 5,
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
        },
        {
            'id': 6,
            'position': (3, 0),
        },
        {
            'id': 7,
            'position': (3, 2),
        },
        {
            'id': 8,
            'position': (4, 0),
            'owner': 'ENEMY',
            'ward': 1,
            'vector': Vector(name='Click', tags=[Boost(1), SpamTrap(count=1)])
        },
        {
            'id': 9,
            'position': (4, 2),
            'owner': 'ENEMY',
            'ward': 1,
            'vector': Vector(name='Warez', tags=[Boost(1), ShovelwareTrap(count=1)])
        },
        {
            'id': 10,
            'position': (5, 1),
            'owner': 'ENEMY',
            'source': True,
            'vector': Vector(name='Warez', tags=[Boost(2), PopupAdTrap(count=2)])
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
            'left_id': 4,
            'right_id': 7
        },
        {
            'left_id': 5,
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
            'left_id': 6,
            'right_id': 9
        },
        {
            'left_id': 7,
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
            'power': 3,
            'vectors': [Vector(name='Warez', default_ward=1, tags=[PopupAdTrap(count=1)])],
            'pathing': PathType.RANDOM,
            'next': lambda prev: 3 if prev == 2 else 2
        },
        {
            'pattern_id': 2,
            'start': True,
            'power': 4,
            'vectors': [
                Vector(name='Clk1', default_ward=1, tags=[ShovelwareTrap(count=1)]),
                Vector(name='Clk2', default_ward=1, tags=[SpamTrap(count=1)])
            ],
            'pathing': PathType.RANDOM,
            'next': lambda prev: 3 if prev == 1 else 1
        },
        {
            'pattern_id': 3,
            'start': True,
            'power': 5,
            'self_tags': [EnemySurge(1)],
            'pathing': PathType.ATTACK_OPPONENT_SOURCE,
            'next': lambda prev: random.choice([1, 2])
        }
    ]
}