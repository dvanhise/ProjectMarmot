import pygame
from src.constants import SCREEN_WIDTH, TERMINAL_GREEN, DARK_TERMINAL
from src.utils.asset_loader import get_font

HELP_LINE_HEIGHT = 14
HELP_TEXT_FONT = 13
TEXT_PADDING = 2
SCREEN_EDGE_BUFFER = 20
CURSOR_OFFSET = 15


def render_help_text(s: pygame.Surface, text_list, left, top):
    font = pygame.font.Font(get_font('BrassMono', 'regular'), HELP_TEXT_FONT)
    text_renders = [font.render(t, True, TERMINAL_GREEN) for t in text_list]
    max_width = max([t.get_size()[0] for t in text_renders])
    height = HELP_LINE_HEIGHT*len(text_renders) + TEXT_PADDING*(len(text_renders) + 1)

    # Adjust left offset to prevent text from going off screen
    new_left = min(left+CURSOR_OFFSET, SCREEN_WIDTH - max_width - SCREEN_EDGE_BUFFER)

    pygame.draw.rect(s, DARK_TERMINAL, pygame.Rect(new_left, top+CURSOR_OFFSET, max_width+2*TEXT_PADDING, height))
    pygame.draw.rect(s, 'white', pygame.Rect(new_left, top+CURSOR_OFFSET, max_width+2*TEXT_PADDING, height), width=1)

    for ndx, render in enumerate(text_renders):
        text_rect = render.get_rect(topleft=(new_left+TEXT_PADDING, top+CURSOR_OFFSET+ndx*(TEXT_PADDING+HELP_LINE_HEIGHT)+TEXT_PADDING))
        s.blit(render, text_rect)
