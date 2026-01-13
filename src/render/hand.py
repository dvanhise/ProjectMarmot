import pygame
from game_objects.player import Player
from render.card import generate as gen_card, CARD_WIDTH, CARD_HEIGHT


HAND_WIDTH = 1000

CARD_GAP = 5


def generate(player: Player):
    s = pygame.Surface((HAND_WIDTH, CARD_HEIGHT))

    for n, card_render in enumerate([gen_card(c) for c in player.get_cards_in_hand()]):
        s.blit(card_render, (n*CARD_WIDTH+n*CARD_GAP, 0))

    return s
