import pygame
from src.game_objects.round_end import RoundEndPick
from src.render.card import gen_card, gen_health_card, CARD_WIDTH, CARD_HEIGHT
from src.utils.text_helper import draw_text_with_outline
from src.utils.asset_loader import get_font
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_TERMINAL, CURRENCY_COLOR


WINDOW_WIDTH = SCREEN_WIDTH - 200
WINDOW_HEIGHT = 500
WINDOW_LEFT = SCREEN_WIDTH//2 - WINDOW_WIDTH//2
WINDOW_TOP = SCREEN_HEIGHT//2 - WINDOW_HEIGHT//2

CARD_GAP = 20
CARD_VERT_OFFSET = WINDOW_HEIGHT//2 - CARD_HEIGHT//2

TEXT_FONT_SIZE = 28
TEXT_VERT_OFFSET = CARD_VERT_OFFSET - 50

BUTTON_SIZE = (160, 40)
BUTTON_VERT_OFFSET = CARD_VERT_OFFSET + CARD_HEIGHT + 50


def render_round_end_screen(s: pygame.Surface, choices: RoundEndPick):
    interactables = {}
    card_count = len(choices)

    # Background and Border
    pygame.draw.rect(s, DARK_TERMINAL, pygame.Rect(WINDOW_LEFT, WINDOW_TOP, WINDOW_WIDTH, WINDOW_HEIGHT), border_radius=5)
    pygame.draw.rect(s, '#444444', pygame.Rect(WINDOW_LEFT, WINDOW_TOP, WINDOW_WIDTH, WINDOW_HEIGHT), width=5, border_radius=5)
    pygame.draw.rect(s, '#CCCCCC', pygame.Rect(WINDOW_LEFT, WINDOW_TOP, WINDOW_WIDTH, WINDOW_HEIGHT), width=2, border_radius=5)

    # Instruction text
    font = pygame.font.Font(get_font('BrassMono', 'regular'), TEXT_FONT_SIZE)
    text = font.render('Infiltration successful, found new tools:', True, 'white')
    text_rect = text.get_rect(center=(WINDOW_LEFT+WINDOW_WIDTH//2, WINDOW_TOP+TEXT_VERT_OFFSET))
    s.blit(text, text_rect)

    card_pick_width = CARD_WIDTH*card_count + CARD_GAP*(card_count-1)
    card_x_offset = WINDOW_LEFT + WINDOW_WIDTH//2 - card_pick_width//2

    # Draw pickable cards
    cost_font = pygame.font.Font(get_font('BrassMono', 'regular'), 24)
    for ndx, choice in enumerate(choices):
        horizontal_offset = card_x_offset + ndx * CARD_WIDTH + ndx * CARD_GAP
        if choice.choice_type == 'card':
            s.blit(gen_card(choice.card), (horizontal_offset, WINDOW_TOP + CARD_VERT_OFFSET))
        elif choice.choice_type == 'remove_card':
            s.blit(gen_card(choice.card), (horizontal_offset, WINDOW_TOP + CARD_VERT_OFFSET))
            font = pygame.font.Font(get_font('BrassMono', 'regular'), 20)
            outline_text = draw_text_with_outline('Remove Card', font, 'red', 2, 'black')
            text_rect = outline_text.get_rect(center=(horizontal_offset+CARD_WIDTH//2, WINDOW_TOP + CARD_VERT_OFFSET+CARD_HEIGHT-30))
            s.blit(outline_text, text_rect)
        elif choice.choice_type == 'health':
            s.blit(gen_health_card(choice.health), (horizontal_offset, WINDOW_TOP + CARD_VERT_OFFSET))
        elif choice.choice_type == 'empty':
            pass

        cost_text = draw_text_with_outline(f'※{choice.cost}', cost_font, CURRENCY_COLOR, 2, 'black')
        text_rect = cost_text.get_rect(center=(horizontal_offset+CARD_WIDTH//2, WINDOW_TOP + CARD_VERT_OFFSET+CARD_HEIGHT+20))
        s.blit(cost_text, text_rect)

        interactables[f'PICK{ndx}'] = pygame.Rect(horizontal_offset, WINDOW_TOP + CARD_VERT_OFFSET, CARD_WIDTH, CARD_HEIGHT)

    # Next button
    button_rect = pygame.Rect((WINDOW_LEFT+WINDOW_WIDTH//2-BUTTON_SIZE[0]//2, WINDOW_TOP+BUTTON_VERT_OFFSET), BUTTON_SIZE)
    pygame.draw.rect(s, '#5CC9D4', button_rect)
    pygame.draw.rect(s, '#444444', button_rect, width=2)
    font = pygame.font.Font(get_font('BrassMono', 'regular'), 20)
    outline_text = draw_text_with_outline('Continue', font, 'white', 2, 'black')
    text_rect = outline_text.get_rect(center=(WINDOW_LEFT+WINDOW_WIDTH//2, WINDOW_TOP+BUTTON_VERT_OFFSET+BUTTON_SIZE[1]//2))
    s.blit(outline_text, text_rect)
    interactables['NEXT_BUTTON'] = button_rect

    return interactables
