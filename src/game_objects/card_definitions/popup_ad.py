from game_objects.card_type import CardType
from game_objects.card import Card


class PopupAd(Card):
    id = 'popup-ad'
    name = 'Popup Ad'
    type = CardType.NULL
    rarity = 'special'
    image_id = 'placeholder'
    cost = 0
    description = ['Unplayable']
