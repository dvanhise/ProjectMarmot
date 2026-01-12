from game_objects.level import Level
from game_objects.deck import Deck
from game_objects.script import Script, ScriptBuilder


class GameState:
    def __init__(self):
        self.deck = Deck()
        self.script_builder = ScriptBuilder()
        self.level = None

    def start_new_level(self, level: Level):
        self.level = level
        self.deck.reset()
        self.deck.draw(5)
        self.script_builder.clear()
