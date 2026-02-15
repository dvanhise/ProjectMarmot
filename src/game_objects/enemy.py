import copy
from typing import Callable

from src.game_objects.script import Script
from src.game_objects.tag import TagManager


class Enemy:
    owner = 'ENEMY'

    def __init__(self, definition):
        self.pattern = {action['pattern_id']: action for action in definition['pattern']}
        self.current_pattern_id = None
        self.previous_pattern_id = None
        self.script = None
        self.portrait = definition['portrait']
        self.health = definition['health']
        self.max_health = definition['health']
        self.tags = TagManager()

    def change_health(self, change):
        self.health = min(self.max_health, max(0, self.health + change))
        
    def next_script(self):
        if self.current_pattern_id is None:
            self.current_pattern_id = [k for k,v in self.pattern.items() if v.get('start')][0]
        else:
            next_pattern = self.pattern[self.current_pattern_id]['next']
            prev = self.previous_pattern_id
            self.previous_pattern_id = self.current_pattern_id
            if type(next_pattern) is Callable:
                self.current_pattern_id = next_pattern(prev)
            elif type(next_pattern) is int:
                self.current_pattern_id = next_pattern
            else:
                raise ValueError(f'Unexpected type for next pattern "{type(next_pattern)}"')

        self.script = Script('ENEMY')
        p = self.pattern[self.current_pattern_id]
        self.script.power = p.get('power', 0)
        self.script.pathing = p['pathing']
        self.tags.on_script_creation(self.script)

        tags = p.get('tags', [])
        for tag in tags:
            self.script.tags.add_tag(tag)

        vectors = p.get('vectors', [])
        for vector in vectors:
            self.script.vector.append(copy.deepcopy(vector))

        return self.script

    def get_enemy_info_dict(self):
        return {
            'health': self.health
        }

    def check_defeat(self):
        return self.health <= 0