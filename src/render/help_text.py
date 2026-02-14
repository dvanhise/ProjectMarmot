import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TERMINAL_GREEN, DARK_TERMINAL
from src.utils.asset_loader import get_font

HELP_HEIGHT = 16
HELP_TEXT_FONT = 12
TEXT_PADDING = 2
SCREEN_EDGE_BUFFER = 20


def render_help_text(s: pygame.Surface, text, left, top):
    font = pygame.font.Font(get_font('BrassMono', 'regular'), HELP_TEXT_FONT)
    text = font.render(text, True, TERMINAL_GREEN)
    text_size = text.get_size()

    new_left = min(left, SCREEN_WIDTH - text_size[0] - SCREEN_EDGE_BUFFER)

    pygame.draw.rect(s, DARK_TERMINAL, pygame.Rect(new_left, top, text_size[0]+2*TEXT_PADDING, HELP_HEIGHT))
    pygame.draw.rect(s, 'white', pygame.Rect(new_left, top, text_size[0]+2*TEXT_PADDING, HELP_HEIGHT), width=1)

    text_rect = text.get_rect(topleft=(new_left+TEXT_PADDING, top+TEXT_PADDING))
    s.blit(text, text_rect)
