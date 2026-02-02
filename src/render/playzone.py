from render.card import CARD_WIDTH, CARD_HEIGHT
from constants import *
from utils.image_loader import img_fetch


SCREEN_OFFSET = (20, SCREEN_HEIGHT // 2 + 80)
ZONE_SIZE = (CARD_WIDTH, CARD_HEIGHT)

FONT_SIZE = 24


def render_playzone(s: pygame.Surface):
    img = img_fetch().get('empty-space')
    img = pygame.transform.smoothscale(img, ZONE_SIZE)
    s.blit(img, SCREEN_OFFSET)

    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', FONT_SIZE)
    text = font.render('Utility', True, 'white')
    text_rect = text.get_rect(center=(SCREEN_OFFSET[0]+ZONE_SIZE[0]//2, SCREEN_OFFSET[1]+ZONE_SIZE[1]//2))
    s.blit(text, text_rect)

    return {'PLAYZONE': pygame.Rect(SCREEN_OFFSET, ZONE_SIZE)}