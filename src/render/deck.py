import pygame
from src.game_objects.deck_category import DeckCategory
from src.render.card import CARD_WIDTH, CARD_HEIGHT, gen_card
from src.utils.asset_loader import get_font
from src.utils.text_helper import draw_text_with_outline
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_TERMINAL


HORIZONTAL_CARDS = 7
VERTICAL_CARDS = 4

PADDING = 15
BUTTON_SIZE = (160, 40)

WINDOW_WIDTH = HORIZONTAL_CARDS*CARD_WIDTH + HORIZONTAL_CARDS*(PADDING+1)
WINDOW_HEIGHT = VERTICAL_CARDS*CARD_HEIGHT + VERTICAL_CARDS*(PADDING+2) + BUTTON_SIZE[1]
WINDOW_LEFT = SCREEN_WIDTH//2 - WINDOW_WIDTH//2
WINDOW_TOP = SCREEN_HEIGHT//2 - WINDOW_HEIGHT//2


def render_deck_screen(s: pygame.Surface, player, category):
    # Background and Border
    pygame.draw.rect(s, DARK_TERMINAL, pygame.Rect(WINDOW_LEFT, WINDOW_TOP, WINDOW_WIDTH, WINDOW_HEIGHT), border_radius=5)
    pygame.draw.rect(s, '#444444', pygame.Rect(WINDOW_LEFT, WINDOW_TOP, WINDOW_WIDTH, WINDOW_HEIGHT), width=5, border_radius=5)
    pygame.draw.rect(s, '#CCCCCC', pygame.Rect(WINDOW_LEFT, WINDOW_TOP, WINDOW_WIDTH, WINDOW_HEIGHT), width=2, border_radius=5)

    if category == DeckCategory.FULL:
        cards = player.get_full_deck()
    elif category == DeckCategory.DRAW:
        cards = player.get_cards_in_draw_pile(seed=1234)
    elif category == DeckCategory.DISCARD:
        cards = player.get_cards_in_discard()
    elif category == DeckCategory.DELETED:
        cards = player.get_deleted_cards()
    else:
        raise ValueError(f'Unknown deck card category: {category}')

    # Render cards
    for ndx, card in enumerate(cards):
        y_pos = ndx // HORIZONTAL_CARDS
        x_pos = ndx % HORIZONTAL_CARDS
        s.blit(gen_card(card), (WINDOW_LEFT+PADDING+x_pos*(CARD_WIDTH+PADDING), WINDOW_TOP+PADDING+y_pos*(CARD_HEIGHT+PADDING)))

    # Render exit button
    button_rect = pygame.Rect((WINDOW_LEFT+WINDOW_WIDTH//2-BUTTON_SIZE[0]//2, WINDOW_TOP+WINDOW_HEIGHT-BUTTON_SIZE[1]-PADDING), BUTTON_SIZE)
    pygame.draw.rect(s, '#5CC9D4', button_rect)
    pygame.draw.rect(s, '#444444', button_rect, width=2)
    font = pygame.font.Font(get_font('BrassMono', 'regular'), 20)
    outline_text = draw_text_with_outline('Done', font, 'white', 2, 'black')
    text_rect = outline_text.get_rect(center=(WINDOW_LEFT+WINDOW_WIDTH//2, WINDOW_TOP+WINDOW_HEIGHT-BUTTON_SIZE[1]//2-PADDING))
    s.blit(outline_text, text_rect)

    return {'LEAVE_DECK': button_rect}
