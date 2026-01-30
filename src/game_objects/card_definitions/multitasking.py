from game_objects.card_type import CardType
from game_objects.tags.multitasking import Multitasking
from utils.action_queue import get_aq


def on_play():
    get_aq().queue_action('add_player_tag', Multitasking, 1)


definition = {
    'id': 'multitasking',
    'name': 'Multi-tasking',
    'type': CardType.UTILITY,
    'rarity': 'default',
    'image_id': 'query',
    'cost': 1,
    'description': ['When executing a script,', 'draw 1 card'],
    'on_play': on_play
}
