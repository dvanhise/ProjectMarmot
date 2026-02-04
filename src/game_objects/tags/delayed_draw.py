from game_objects.tag import Tag
from utils.action_queue import get_aq


class DelayedDraw(Tag):
    id = 'delayed-draw'
    name = 'Delayed Draw'
    icon = 'power'
    tooltip = 'At the start of next turn, draw {count} cards.'

    def on_turn_start_player(self, player):
        player.draw(self.count)
        self.count = 0
