import pygame
from src.utils.asset_loader import get_font
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TERMINAL_GREEN


FONT_SIZE = 60

LINE_OFFSET = 50


def render_end_screen(s: pygame.Surface, win=True):
    font = pygame.font.Font(get_font('BrassMono', 'bold'), FONT_SIZE)
    text = font.render('YOU WIN' if win else 'YOU LOSE', True, TERMINAL_GREEN)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    s.blit(text, text_rect)

    text = font.render('YOU ARE THE BEST HACKER!' if win else 'YOU WERE SLAIN OVER THE INTERNET', True, TERMINAL_GREEN)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+ LINE_OFFSET))
    s.blit(text, text_rect)