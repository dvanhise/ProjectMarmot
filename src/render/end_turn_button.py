import pygame
from utils.image_loader import img_fetch
from render.constants import *


BUTTON_SIZE = (100, 100)
LABEL_FONT_SIZE = 20


def render_end_turn(s: pygame.Surface):
    x = SCREEN_WIDTH - BUTTON_SIZE[0] - 20
    y = SCREEN_HEIGHT - BUTTON_SIZE[1] - 20

    image = img_fetch().get('button')
    image = pygame.transform.smoothscale(image, BUTTON_SIZE)
    s.blit(image, (x, y))

    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', LABEL_FONT_SIZE)
    text = font.render('End Turn', True, 'white')
    text_rect = text.get_rect(center=(x + BUTTON_SIZE[0]//2, y + BUTTON_SIZE[1]//2))
    s.blit(text, text_rect)

    return {'END_TURN': pygame.Rect(x, y, BUTTON_SIZE[0], BUTTON_SIZE[1])}
