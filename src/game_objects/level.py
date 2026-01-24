from game_objects.graph import Node, Edge
from game_objects.script import Script


class Level:
    def __init__(self, definition):
        self.pattern = {action['pattern_id']: action for action in definition['pattern']}
        self.current_pattern_id = None
        self.planned_script = None
        self.edge_difficulty = definition.get('edge_difficulty', 1)
        self.network_width = definition['network_width']
        self.network_height = definition['network_height']
        self.portrait = 'avatar2'  # FIXME
        self.health = definition['health']

        self.nodes = {node['id']: Node(**node) for node in definition['nodes']}

        for e in definition['edges']:
            edge = Edge(self.nodes[e['left_id']], self.nodes[e['right_id']], e.get('difficulty', self.edge_difficulty))
            self.nodes[e['left_id']].right.append(edge)
            self.nodes[e['right_id']].left.append(edge)


    def next_script(self):
        if self.current_pattern_id is None:
            self.current_pattern_id = [k for k,v in self.pattern.items() if v.get('start')][0]
        else:
            # TODO: Allow for RNG-based patterns
            self.current_pattern_id = self.pattern[self.current_pattern_id]['next']

        self.planned_script = Script('ENEMY')
        p = self.pattern[self.current_pattern_id]
        self.planned_script.power = p.get('power', 0)
        vector = p.get('vector')
        if vector:
            self.planned_script.vector.append(vector)

        return self.planned_script

    def get_source(self, owner):
        for node in self.nodes.values():
            if node.owner == owner and node.source:
                return node

        return None

    def check_victory(self):
        return self.health <= 0
