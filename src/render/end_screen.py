import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TERMINAL_GREEN


FONT_SIZE = 50


def render_end_screen(s: pygame.Surface, win=True):
    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', FONT_SIZE)
    text = font.render('YOU WIN' if win else 'YOU LOSE', True, TERMINAL_GREEN)
    text_rect = text.get_rect(center=(SCREEN_WIDTH, SCREEN_HEIGHT))
    s.blit(text, text_rect)