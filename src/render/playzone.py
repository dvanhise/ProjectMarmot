from render.card import CARD_HEIGHT
from constants import *
from utils.image_loader import img_fetch


SCREEN_OFFSET = (20, SCREEN_HEIGHT // 2 + 20)
ZONE_SIZE = (int(CARD_HEIGHT*1.5), CARD_HEIGHT)


def render_playzone(s: pygame.Surface):
    img = img_fetch().get('playzone')
    img = pygame.transform.smoothscale(img, ZONE_SIZE)
    s.blit(img, SCREEN_OFFSET)
    return {'PLAYZONE': pygame.Rect(SCREEN_OFFSET, ZONE_SIZE)}