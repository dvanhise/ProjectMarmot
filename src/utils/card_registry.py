import os
import importlib
import random
from game_objects.card import Card


CARD_DEF_DIR = './src/game_objects/card_definitions'
CARD_DEF_PATH = 'game_objects.card_definitions'


card_registry = {}

# Get all python files in the directory
card_files = os.listdir(CARD_DEF_DIR)
card_files = [f.replace('.py', '') for f in card_files if f.endswith('.py')]

for f in card_files:
    card = importlib.import_module(f'{CARD_DEF_PATH}.{f}')
    card_registry[card.definition['id']] = card.definition


def get_new_card(name):
    if name not in card_registry:
        raise KeyError(f'Card "{name}" not found in card registry.')

    return Card(**card_registry[name])


def random_card_choices(count):
    available_cards = [c for c in list(card_registry.values()) if c['rarity'] in ['simple', 'intermediate', 'elite']]
    card_sample = random.sample(available_cards, count)
    return [Card(**c) for c in card_sample]
