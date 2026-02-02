from game_objects.graph import Node, Edge
from game_objects.script import Script
from game_objects.tag import TagManager


class Level:
    def __init__(self, definition):
        self.pattern = {action['pattern_id']: action for action in definition['pattern']}
        self.current_pattern_id = None
        self.planned_script = None
        self.edge_difficulty = definition.get('edge_difficulty', 1)
        self.network_width = definition['network_width']
        self.network_height = definition['network_height']
        self.portrait = definition['portrait']
        self.health = definition['health']
        self.tags = TagManager()

        self.nodes = {node['id']: Node(**node) for node in definition['nodes']}

        for e in definition['edges']:
            owner = 'NEUTRAL'
            if self.nodes[e['left_id']].owner == self.nodes[e['right_id']].owner:
                owner = self.nodes[e['left_id']].owner
            edge = Edge(self.nodes[e['left_id']], self.nodes[e['right_id']], e.get('difficulty', self.edge_difficulty), owner)
            self.nodes[e['left_id']].right.append(edge)
            self.nodes[e['right_id']].left.append(edge)


    def get_source(self, owner):
        for node in self.nodes.values():
            if node.owner == owner and node.source:
                return node

        return None

    def check_win(self):
        return self.health <= 0
