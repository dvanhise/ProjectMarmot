from src.game_objects.level_definitions.haxor import definition as level1_def
from src.game_objects.level_definitions.glitch_masta import definition as level2_def
from src.game_objects.level_definitions.sword_shield import definition as level3_def
from src.game_objects.level_definitions.free_warez import definition as level4_def
from src.game_objects.level_definitions.panopticorp import definition as level5_def
from src.game_objects.level_definitions.billionz import definition as level6_def


def get_level_order():
    return [
        level1_def,
        level2_def,
        level3_def,
        level4_def,
        level5_def,
        level6_def
    ]