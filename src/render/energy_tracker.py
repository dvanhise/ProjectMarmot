import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, ENERGY_COLOR
from src.render.card import CARD_HEIGHT
from src.utils.text_helper import draw_text_with_outline
from src.utils.asset_loader import get_font

SCREEN_OFFSET = (SCREEN_WIDTH-50, SCREEN_HEIGHT - CARD_HEIGHT + 20)
ENERGY_CIRCLE_RADIUS = 30
ENERGY_FONT_SIZE = 26


def render_energy_tracker(s: pygame.Surface, player):
    pygame.draw.circle(s, ENERGY_COLOR, SCREEN_OFFSET, ENERGY_CIRCLE_RADIUS)
    font = pygame.font.Font(get_font('BrassMono', 'bold'), ENERGY_FONT_SIZE)
    energy_text = draw_text_with_outline(f'{player.energy}/{player.max_energy}', font, 'white', 2, 'black')
    text_rect = energy_text.get_rect(center=SCREEN_OFFSET)
    s.blit(energy_text, text_rect)