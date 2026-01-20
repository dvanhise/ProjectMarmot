import pygame
from render.constants import *
from render.card import CARD_HEIGHT, CARD_WIDTH

SCREEN_OFFSET = (140, SCREEN_HEIGHT - CARD_HEIGHT + 20)
ENERGY_CIRCLE_COLOR = pygame.Color('#AA00AA')
ENERGY_CIRCLE_RADIUS = 30
ENERGY_FONT_SIZE = 32


def render_energy_tracker(s: pygame.Surface, player):
    pygame.draw.circle(s, ENERGY_CIRCLE_COLOR, SCREEN_OFFSET, ENERGY_CIRCLE_RADIUS)
    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', ENERGY_FONT_SIZE)
    text = font.render(str(player.energy), True, 'white')
    text_rect = text.get_rect(center=SCREEN_OFFSET)
    s.blit(text, text_rect)