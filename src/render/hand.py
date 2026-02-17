import pygame
from src.game_objects.player import Player
from src.render.card import gen_card, CARD_WIDTH, CARD_HEIGHT
from src.utils.mouse_check import Tooltip
from src.constants import SCREEN_HEIGHT


PADDING = 5


def render_hand(s: pygame.Surface, player: Player):
    interactables = {}
    mouseover = []
    card_count = len(player.current_hand)

    # Adjust gap/overlap between cards to allow a full hand to fit
    if card_count <= 7:
        card_gap = 5
    elif card_count == 8:
        card_gap = 0
    elif card_count == 9:
        card_gap = -10
    else:
        card_gap = -25


    hand_surface = pygame.Surface((CARD_WIDTH*card_count + card_gap*(card_count-1), CARD_HEIGHT))

    screen_offset = (PADDING, SCREEN_HEIGHT-CARD_HEIGHT-PADDING)

    for n, card in enumerate(player.get_cards_in_hand()):
        card_render = gen_card(card)
        horizontal_offset = n*CARD_WIDTH+n*card_gap
        hand_surface.blit(card_render, (horizontal_offset, 0))
        interactables[f'CARD{n}'] = pygame.Rect(screen_offset[0] + horizontal_offset, screen_offset[1], CARD_WIDTH, CARD_HEIGHT)

        mouseover.append(
            Tooltip(pygame.Rect(screen_offset[0] + horizontal_offset, screen_offset[1], CARD_WIDTH, CARD_HEIGHT),
                    [f'{tag.name}: {tag.tooltip.format(count='X', card='Card')}' for tag in card.tooltips])
        )

    s.blit(hand_surface, screen_offset)

    return interactables, mouseover
