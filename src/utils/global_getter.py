from game_objects.player import Player
from game_objects.enemy import Enemy
from game_objects.level import Level
from game_objects.script import ScriptBuilder


player = None
enemy = None
level = None
script_builder = None


def get_player():
    global player
    if not player:
        player = Player()
    return player

def new_enemy(enemy_def):
    global enemy
    enemy = Enemy(enemy_def)
    return enemy

def get_enemy():
    global enemy
    return enemy

def new_level(level_def):
    global level
    level = Level(level_def)
    return level

def get_level():
    global level
    return level

def get_script_builder():
    global script_builder
    if not script_builder:
        script_builder = ScriptBuilder()
    return script_builder
