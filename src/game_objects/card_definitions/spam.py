from src.game_objects.card_type import CardType
from src.game_objects.card import Card


class Spam(Card):
    id = 'spam'
    name = 'Spam'
    type = CardType.NULL
    rarity = 'special'
    image_id = 'placeholder'
    cost = '-'
    description = ['Unplayable']
