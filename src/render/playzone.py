from src.render.card import CARD_WIDTH, CARD_HEIGHT
from src.render.network import NETWORK_HEIGHT
from src.constants import *
from src.utils.asset_loader import img_fetch, get_font

SCREEN_OFFSET = (20, NETWORK_HEIGHT + 10)
ZONE_SIZE = (CARD_WIDTH, CARD_HEIGHT)

FONT_SIZE = 24


def render_playzone(s: pygame.Surface):
    img = img_fetch().get('empty-space')
    img = pygame.transform.smoothscale(img, ZONE_SIZE)
    s.blit(img, SCREEN_OFFSET)

    font = pygame.font.Font(get_font('BrassMono', 'regular'), FONT_SIZE)
    text = font.render('Utility', True, 'white')
    text_rect = text.get_rect(center=(SCREEN_OFFSET[0]+ZONE_SIZE[0]//2, SCREEN_OFFSET[1]+ZONE_SIZE[1]//2))
    s.blit(text, text_rect)

    return {'PLAYZONE': pygame.Rect(SCREEN_OFFSET, ZONE_SIZE)}