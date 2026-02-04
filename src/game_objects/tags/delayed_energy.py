from game_objects.tag import Tag
from utils.action_queue import get_aq


class DelayedEnergy(Tag):
    id = 'delayed-energy'
    name = 'Delayed Energy'
    icon = 'power'
    tooltip = 'At the start of next turn, gain {count} energy.'

    def on_turn_start_player(self, player):
        player.energy += self.count
        self.count = 0
