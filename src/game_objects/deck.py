from random import shuffle
import logging
from game_objects.card import Card


class Deck:
    def __init__(self):
        self.id_counter = 0
        self.all_cards = {}
        self.temp_cards = []
        self.draw_pile = []
        self.current_hand = []
        self.discard_pile = []
        self.dragged = None

    def get_full_deck(self):
        return list(self.all_cards.values())

    def get_cards_in_hand(self):
        return [self.all_cards[card_id] for card_id in self.current_hand]

    def get_cards_in_discard(self):
        return [self.all_cards[card_id] for card_id in self.discard_pile]

    def get_cards_in_draw_pile(self):
        return [self.all_cards[card_id] for card_id in self.draw_pile]

    def add_card(self, new_card: Card):
        self.all_cards[self.id_counter] = new_card
        self.id_counter += 1

    def remove_card(self, card_id):
        card = self.all_cards[card_id]
        del self.all_cards[card_id]
        return card

    def reset(self):
        self.current_hand = []
        self.discard_pile = []
        self.draw_pile = list(self.all_cards.keys())
        shuffle(self.draw_pile)

    def discard_hand(self):
        discarded = self.current_hand
        self.discard_pile += discarded
        self.current_hand = []
        return discarded

    def add_card_to_discard(self, card_id):
        pass

    def add_temp_card(self):
        pass

    def draw(self, count):
        for _ in range(count):
            self.current_hand.append(self.draw_pile.pop(0))

    def start_drag(self, card_id):
        if card_id not in self.current_hand:
            logging.error(f'Card ID "{card_id}" not found in current hand "{self.current_hand}"')
            return

        self.dragged = card_id
        self.current_hand.remove(card_id)
