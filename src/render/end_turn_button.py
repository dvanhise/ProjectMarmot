from src.utils.asset_loader import img_fetch
from src.constants import *


BUTTON_SIZE = (80, 80)
LABEL_FONT_SIZE = 20


def render_end_turn(s: pygame.Surface):
    x = SCREEN_WIDTH - BUTTON_SIZE[0] - 10
    y = SCREEN_HEIGHT - BUTTON_SIZE[1] - 5

    image = img_fetch().get('end-turn')
    image = pygame.transform.smoothscale(image, BUTTON_SIZE)
    s.blit(image, (x, y))

    return {'END_TURN': pygame.Rect(x, y, BUTTON_SIZE[0], BUTTON_SIZE[1])}
