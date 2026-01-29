from game_objects.vector import Vector

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
            'position': (2, 0),
            'owner': 'ENEMY',
            'vector': Vector(name='Amp', power_boost=2)
        },
        {
            'id': 5,
            'position': (2, 2),
            'owner': 'ENEMY',
            'vector': Vector(name='Amp', power_boost=2)
        },
        {
            'id': 6,
            'position': (2, 4),
            'owner': 'ENEMY',
            'vector': Vector(name='Amp', power_boost=2)
        },
        {
            'id': 7,
            'position': (3, 1),
            'owner': 'ENEMY',
            'vector': Vector(name='Amp', power_boost=2)
        },
        {
            'id': 8,
            'name': 'Database',
            'position': (3, 3),
            'owner': 'ENEMY',
            'vector': Vector(name='Amp', power_boost=2)
        },
        {
            'id': 9,
            'position': (4, 2),
            'owner': 'ENEMY',
            'vector': Vector(name='Amp', power_boost=2),
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
            'right_id': 7,
            'owner': 'ENEMY'
        },
        {
            'left_id': 5,
            'right_id': 7,
            'owner': 'ENEMY'
        },
        {
            'left_id': 5,
            'right_id': 8,
            'owner': 'ENEMY'
        },
        {
            'left_id': 6,
            'right_id': 8,
            'owner': 'ENEMY'
        },
        {
            'left_id': 7,
            'right_id': 9,
            'owner': 'ENEMY'
        },
        {
            'left_id': 8,
            'right_id': 9,
            'owner': 'ENEMY'
        }
    ],
    'pattern': [
        {
            'pattern_id': 1,
            'start': True,
            'power': 4,
            'targeting': 'RANDOM',
            'next': 2
        },
        {
            'pattern_id': 2,
            'power': 5,
            'targeting': 'RANDOM',
            'next': 1
        }
    ]
}
