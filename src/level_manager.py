from src.game_objects.level_definitions.level1 import definition as level1_def
from src.game_objects.level_definitions.level2 import definition as level2_def
from src.game_objects.level_definitions.level3 import definition as level3_def
from src.game_objects.level_definitions.level4 import definition as level4_def
from src.game_objects.level_definitions.level5 import definition as level5_def
from src.game_objects.level_definitions.level6 import definition as level6_def


def get_level_order():
    return [
        level1_def,
        level4_def,
        level2_def,
        level6_def,
        level5_def,
        level3_def
    ]