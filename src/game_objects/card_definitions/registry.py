from game_objects.card_definitions import payload1
from game_objects.card import Card

card_registry = {
    'payload1': payload1
}

def get_new_card(name):
    return Card(**(card_registry[name].definition))