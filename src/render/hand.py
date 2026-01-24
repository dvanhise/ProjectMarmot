from game_objects.player import Player
from render.card import generate as gen_card, CARD_WIDTH, CARD_HEIGHT
from constants import *


HAND_WIDTH = 1000

CARD_GAP = 5


def render_hand(s: pygame.Surface, player: Player):
    interactables = {}
    card_count = len(player.current_hand)
    hand_surface = pygame.Surface((CARD_WIDTH*card_count + CARD_GAP*(card_count-1), CARD_HEIGHT))

    screen_offset = (SCREEN_WIDTH//2 - hand_surface.get_width()//2, SCREEN_HEIGHT-CARD_HEIGHT-CARD_GAP)

    for n, card_render in enumerate([gen_card(c) for c in player.get_cards_in_hand()]):
        horizontal_offset = n*CARD_WIDTH+n*CARD_GAP
        hand_surface.blit(card_render, (horizontal_offset, 0))
        interactables[f'CARD{n}'] = pygame.Rect(screen_offset[0] + horizontal_offset, screen_offset[1], CARD_HEIGHT, CARD_HEIGHT)

    s.blit(hand_surface, screen_offset)

    return interactables
