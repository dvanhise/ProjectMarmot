import copy
from random import shuffle
import logging
from src.game_objects.card import Card
from src.game_objects.tag import TagManager


class Player:
    owner = 'PLAYER'

    def __init__(self):
        self.id_counter = 0
        self.all_cards = {}  # Store of permanent cards and their base stats
        self.all_cards_temp = {}  # Copy of all cards during a round that can be temporarily modified
        self.draw_pile = []
        self.current_hand = []
        self.discard_pile = []
        self.deleted_pile = []
        self.dragged = None

        self.energy = 0
        self.max_energy = 3
        self.max_hand_size = 8   # TODO: Change to 10 when screen is larger
        self.draw_count = 5   # Default draw number at start of turn
        self.card_reward_count = 3
        self.tags = TagManager()
        self.script = None

        self.portrait = 'avatar1'
        self.health = 6
        self.max_health = 6
        self.cred = 1  # General currency

    def start_turn(self):
        self.draw(self.draw_count)
        self.energy += self.max_energy

    def init_round(self):
        self.all_cards_temp = copy.deepcopy(self.all_cards)
        for card in self.all_cards_temp:
            self.tags.on_temp_card_creation(card, self.get_player_info_dict())

    def change_health(self, change):
        self.health = min(self.max_health, max(0, self.health + change))

    def has_energy(self, cost):
        return cost <= self.energy

    def pay_energy(self, cost):
        self.energy -= cost

    def end_turn(self):
        self.discard_hand()
        self.energy = 0

    def get_dragged_card(self):
        return self.all_cards_temp[self.dragged]

    def get_full_deck(self):
        return list(self.all_cards_temp.values())

    def get_cards_in_hand(self):
        return [self.all_cards_temp[card_id] for card_id in self.current_hand]

    def get_cards_in_discard(self):
        return [self.all_cards_temp[card_id] for card_id in self.discard_pile]

    def get_cards_in_draw_pile(self):
        return [self.all_cards_temp[card_id] for card_id in self.draw_pile]

    def add_card(self, new_card: Card):
        # For new cards in between rounds
        self.all_cards[self.id_counter] = new_card
        self.id_counter += 1

    def add_temp_card(self, new_card: Card, to: str):
        self.tags.on_temp_card_creation(new_card, self.get_player_info_dict())
        self.all_cards_temp[self.id_counter] = new_card
        if to == 'hand': self.current_hand.append(self.id_counter)
        elif to == 'discard': self.discard_pile.append(self.id_counter)
        elif to == 'draw': self.draw_pile.append(self.id_counter)
        else:
            raise ValueError(f'Unexpected location to add temp card "{to}"')
        self.id_counter += 1

    def remove_card(self, card_id):
        # Permanently remove card from the deck
        card = self.all_cards[card_id]
        del self.all_cards[card_id]
        return card

    def reset(self):
        self.current_hand = []
        self.discard_pile = []
        self.deleted_pile = []
        self.draw_pile = list(self.all_cards.keys())
        shuffle(self.draw_pile)
        self.energy = 0

    def discard_hand(self):
        discarded = self.current_hand
        self.discard_pile += discarded
        self.current_hand = []
        return discarded

    def add_card_to_discard(self, card_id: int):
        self.discard_pile.append(card_id)

    def add_card_to_hand(self, card_id: int):
        self.current_hand.append(card_id)

    def draw(self, count):
        for _ in range(count):
            if len(self.draw_pile) == 0:

                # Stop drawing cards if draw and discard are empty
                if len(self.discard_pile) == 0:
                    break

                # Reshuffle discard into draw if draw is empty
                self.draw_pile = self.discard_pile
                self.discard_pile = []
                shuffle(self.draw_pile)

            if len(self.current_hand) >= self.max_hand_size:
                # Don't draw over max hand size
                self.discard_pile.append(self.draw_pile.pop(0))
            else:
                self.current_hand.append(self.draw_pile.pop(0))

    def start_drag(self, card_id):
        if card_id not in self.current_hand:
            logging.error(f'Card ID "{card_id}" not found in current hand "{self.current_hand}"')
            return

        logging.info(f'Start dragging "{card_id}"')
        self.dragged = card_id
        self.current_hand.remove(card_id)

    def play_card_generic(self, card_id):
        self.dragged = None
        card = self.all_cards_temp[card_id]
        card.on_play()
        self.post_card_played(card_id)

    def post_card_played(self, card_id):
        card = self.all_cards_temp[card_id]
        if card.delete_on_play:
            self.deleted_pile.append(card_id)
        else:
            self.add_card_to_discard(card_id)

    def check_defeat(self):
        return self.health <= 0

    def get_player_info_dict(self):
        return {
            'cards_in_hand': len(self.current_hand),
            'cards_in_discard': len(self.discard_pile),
            'cards_in_draw': len(self.draw_pile),
            'health': self.health,
            'energy': self.energy
        }