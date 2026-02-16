import pygame
from src.game_objects.player import Player
from src.render.card import gen_card, CARD_WIDTH, CARD_HEIGHT
from src.utils.mouse_check import Tooltip
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


CARD_GAP = 5


def render_hand(s: pygame.Surface, player: Player):
    interactables = {}
    mouseover = []
    card_count = len(player.current_hand)
    hand_surface = pygame.Surface((CARD_WIDTH*card_count + CARD_GAP*(card_count-1), CARD_HEIGHT))

    screen_offset = (CARD_GAP, SCREEN_HEIGHT-CARD_HEIGHT-CARD_GAP)

    for n, card in enumerate(player.get_cards_in_hand()):
        card_render = gen_card(card)
        horizontal_offset = n*CARD_WIDTH+n*CARD_GAP
        hand_surface.blit(card_render, (horizontal_offset, 0))
        interactables[f'CARD{n}'] = pygame.Rect(screen_offset[0] + horizontal_offset, screen_offset[1], CARD_WIDTH, CARD_HEIGHT)

        mouseover.append(
            Tooltip(pygame.Rect(screen_offset[0] + horizontal_offset, screen_offset[1], CARD_WIDTH, CARD_HEIGHT),
                    [f'{tag.name}: {tag.tooltip.format(count='N', card='Card')}' for tag in card.tooltips])
        )

    s.blit(hand_surface, screen_offset)

    return interactables, mouseover
