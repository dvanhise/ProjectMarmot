"""
    0   1   2   3   4
0           [4]
1       [2]     [7]
2   [1p]    [5]     [9e]
3       [3]     [8]
4           [6]
"""


nodes = [
    {
        'id': 1,
        'position': (0, 2),
        'owner': 'PLAYER',
        'player_source': True
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
        'ward': 4
    },
    {
        'id': 9,
        'position': (4, 2),
        'owner': 'ENEMY',
        'enemy_source': True
    }
]


edges = [
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
        'right_id': 9,
        'owner': 'ENEMY'
    }
]


pattern = [
    {
        'pattern_id': 1,
        'power': 4,
        'vector': '+1|W2',
        'targeting': 'RANDOM',
        'next': 2
    },
    {
        'pattern_id': 2,
        'power': 6,
        'targeting': 'AGRO',
        'next': 1
    }
]


other = {
    'edge_difficulty': 2,
    'board_width': 5,
    'board_height': 5
}


definition = (nodes, edges, pattern, other)