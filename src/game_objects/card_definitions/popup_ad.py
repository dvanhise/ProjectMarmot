from src.game_objects.card_type import CardType
from src.game_objects.card import Card


class PopupAd(Card):
    id = 'popup-ad'
    name = 'Popup Ad'
    type = CardType.UTILITY
    rarity = 'special'
    image_id = 'placeholder'
    cost = 1
    description = ['Delete when played']
    delete_on_play = True
