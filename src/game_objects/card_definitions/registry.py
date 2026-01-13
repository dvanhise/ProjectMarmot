import os
import importlib
import logging
from game_objects.card import Card


CARD_DEF_DIR = 'game_objects/card_definitions'
CARD_DEF_PATH = 'game_objects.card_definitions'


card_registry = {}

# Get all python files in this directory excluding this one
card_files = os.listdir(CARD_DEF_DIR)
card_files = [f.replace('.py', '') for f in card_files if f != __file__ and f.endswith('.py')]

for f in card_files:
    card = importlib.import_module(f'{CARD_DEF_PATH}.{f}')
    card_registry[card.definition['id']] = card.definition


def get_new_card(name):
    if name not in card_registry:
        logging.error(f'Card "{name}" not found in card registry.')
        return None

    return Card(**card_registry[name])
