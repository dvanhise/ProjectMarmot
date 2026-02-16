import random
import logging
from dataclasses import dataclass
from src.game_objects.card import Card
from src.utils.card_registry import get_random_card


class RoundEndPick(list):
    WEIGHTS = [30, 18, 12, 27, 13]
    OPTIONS = ['card_simple', 'card_intermediate', 'card_elite', 'remove_card', 'health']
    COUNT = 7
    COSTS = [0, 0, random.choice([0,1]), 1, random.choice([1,2]), 2, 2]

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.player = kwargs['player']

        choices = random.choices(self.OPTIONS, weights=self.WEIGHTS, k=self.COUNT)
        for ndx, choice in enumerate(choices):
            if choice.startswith('card'):
                self.append(RoundEndChoice(choice_type='card', cost=self.COSTS[ndx], card=get_random_card(choice.replace('card_', ''))))
            elif choice == 'remove_card':
                # Ensure we don't have two card removal choices for the same card
                current_removals = [x.card_id for x in self if x.choice_type == 'remove_card']
                card_id = random.choice([c for c in self.player.all_cards.keys() if c not in current_removals])
                self.append(RoundEndChoice(choice_type='remove_card', cost=self.COSTS[ndx], card=self.player.all_cards[card_id], card_id=card_id))
            elif choice == 'health':
                self.append(RoundEndChoice(choice_type='health', cost=self.COSTS[ndx], health=random.choice([1,2])))

    def pick(self, ndx):
        choice = self[ndx]
        if choice.choice_type == 'empty':
            logging.warning(f'Cannot purchase empty slot.')
            return

        if choice.cost > self.player.cred:
            logging.warning(f'Unable to afford card.  Have {self.player.cred}, need {choice.cost}.')
            return

        self.player.cred -= choice.cost
        if choice.choice_type == 'card':
            self.player.add_card(choice.card)
        elif choice.choice_type == 'remove_card':
            self.player.remove_card(choice.card_id)
        elif choice.choice_type == 'health':
            self.player.change_health(choice.health)

        choice.choice_type = 'empty'


@dataclass
class RoundEndChoice:
    choice_type: str  # card, remove_card, health, empty
    cost: int
    card: Card = None
    card_id: int = None
    health: int = None
