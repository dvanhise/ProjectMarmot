import pygame
from render.card import generate as gen_card, CARD_WIDTH, CARD_HEIGHT
from utils.text_helper import draw_text_with_outline
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_TERMINAL


WINDOW_WIDTH = SCREEN_WIDTH-400
WINDOW_HEIGHT = SCREEN_HEIGHT-200

CARD_GAP = 20

TEXT_FONT_SIZE = 28
TEXT_VERT_OFFSET = 40

BUTTON_SIZE = (100, 40)
BUTTON_VERT_OFFSET = 30


def render_card_pick(s: pygame.Surface, card_choices):
    interactables = {}
    card_count = len(card_choices)
    card_pick_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Background and Border
    pygame.draw.rect(card_pick_surface, DARK_TERMINAL, pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.draw.rect(card_pick_surface, '#444444', pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), width=5)
    pygame.draw.rect(card_pick_surface, '#CCCCCC', pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), width=2)

    screen_offset = (SCREEN_WIDTH // 2 - WINDOW_WIDTH // 2, SCREEN_HEIGHT // 2 - WINDOW_HEIGHT // 2)
    width = CARD_WIDTH*card_count + CARD_GAP*(card_count-1)
    x_offset = WINDOW_WIDTH//2 - width//2
    y_offset = WINDOW_HEIGHT//2 - CARD_HEIGHT//2

    # Instruction text
    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', TEXT_FONT_SIZE)
    text = font.render('Choose Cards', True, 'white')
    text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y_offset-TEXT_VERT_OFFSET))
    s.blit(text, text_rect)

    # Next button
    button_rect = pygame.Rect((x_offset+width//2-BUTTON_SIZE[0]//2, y_offset+CARD_HEIGHT+BUTTON_VERT_OFFSET), BUTTON_SIZE)
    pygame.draw.rect(card_pick_surface, '#5CC9D4', button_rect)
    pygame.draw.rect(card_pick_surface, '#444444', button_rect, width=2)
    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', 20)
    outline_text = draw_text_with_outline('Continue ->', font, 'white', 2, 'black')
    text_rect = outline_text.get_rect(center=(x_offset+width//2, y_offset+CARD_HEIGHT+BUTTON_VERT_OFFSET+BUTTON_SIZE[1]//2))
    s.blit(outline_text, text_rect)
    interactables['NEXT_BUTTON'] = button_rect

    for n, card_render in enumerate([gen_card(c) for c in card_choices]):
        horizontal_offset = x_offset+n*CARD_WIDTH+n*CARD_GAP
        card_pick_surface.blit(card_render, (horizontal_offset, 0))
        interactables[f'PICK_CARD{n}'] = pygame.Rect(screen_offset[0] + horizontal_offset, screen_offset[1] + y_offset, CARD_WIDTH, CARD_HEIGHT)

    s.blit(card_pick_surface, screen_offset)

    return interactables
