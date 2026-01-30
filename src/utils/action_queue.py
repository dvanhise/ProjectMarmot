aq = None


class ActionQueue:
    ACTIONS = {
        'add_card': 2,  # name, hand/draw/discard
        'draw_cards': 1,   # count
        'change_player_health': 1,  # +/-HP change
        'change_enemy_health': 1,  # +/-HP change
        'execute_script': 0,
        'change_energy': 1,  # +/- energy change
        'add_player_tag': 2,  # tag class, count   TODO: Could be tags with more arguments
        'add_enemy_tag': 2,  # tag class, count
    }

    def __init__(self):
        self.queue = []

    def queue_action(self, action: str, *args):
        if action not in self.ACTIONS.keys():
            raise KeyError(f'Invalid action "{action}"')

        if len(args) != self.ACTIONS[action]:
            raise ValueError(f'Invalid arguments for action "{action}", expected {self.ACTIONS[action]}, found {len(args)}')

        self.queue.append([action, *args])

    def get_action(self):
        if not len(self.queue):
            return None
        return self.queue.pop(0)


def get_aq():
    global aq
    if not aq:
        aq = ActionQueue()
    return aq