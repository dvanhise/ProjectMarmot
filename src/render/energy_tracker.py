import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ENERGY_COLOR
from render.card import CARD_HEIGHT

SCREEN_OFFSET = (SCREEN_WIDTH-50, SCREEN_HEIGHT - CARD_HEIGHT + 20)
ENERGY_CIRCLE_RADIUS = 30
ENERGY_FONT_SIZE = 20


def render_energy_tracker(s: pygame.Surface, player):
    pygame.draw.circle(s, ENERGY_COLOR, SCREEN_OFFSET, ENERGY_CIRCLE_RADIUS)
    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', ENERGY_FONT_SIZE)
    text = font.render(f'{player.energy} Energy', True, 'white')
    text_rect = text.get_rect(center=SCREEN_OFFSET)
    s.blit(text, text_rect)