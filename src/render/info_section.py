from src.game_objects.player import Player
from src.game_objects.enemy import Enemy
from src.render.tag import gen_tag, TAG_ICON_SIZE
from src.utils.asset_loader import img_fetch, get_font
from src.utils.mouse_check import Tooltip
from src.constants import *


INFO_SECTION_SIZE = (120, 160)

PORTRAIT_SIZE = (100, 100)

SCREEN_OFFSET_PLAYER = (30, 30)
SCREEN_OFFSET_ENEMY = (SCREEN_WIDTH - PORTRAIT_SIZE[0] - 30, 30)

HEALTH_FONT_SIZE = 24


def render_info(s: pygame.Surface, entity: Player|Enemy):
    if entity.owner == 'PLAYER':
        offset = SCREEN_OFFSET_PLAYER
    elif entity.owner == 'ENEMY':
        offset = SCREEN_OFFSET_ENEMY
    else:
        raise ValueError(f'Unexpected entity type "{entity.owner}"')

    mouseover = []

    # Draw portait and border
    img = img_fetch().get(entity.portrait)
    img = pygame.transform.smoothscale(img, PORTRAIT_SIZE)
    s.blit(img, offset)
    pygame.draw.rect(s, '#444444', pygame.Rect(offset, PORTRAIT_SIZE), 5, 5)
    pygame.draw.rect(s, '#DDDDDD', pygame.Rect(offset, PORTRAIT_SIZE), 3, 5)

    # Draw health
    font = pygame.font.Font(get_font('BrassMono', 'bold'), HEALTH_FONT_SIZE)
    text = font.render(f'{entity.health} HP', True, 'white')
    text_rect = text.get_rect(center=(offset[0]+PORTRAIT_SIZE[0]//2, offset[1]+PORTRAIT_SIZE[1]-10))
    s.blit(text, text_rect)

    # Draw tags
    for ndx, tag in enumerate(entity.tags):
        s.blit(gen_tag(tag), (offset[0]+ndx*TAG_ICON_SIZE[0], offset[1]+PORTRAIT_SIZE[1]))
        mouseover.append(Tooltip(
            pygame.Rect((offset[0]+ndx*TAG_ICON_SIZE[0], offset[1]+PORTRAIT_SIZE[1]), TAG_ICON_SIZE),
            tag.get_tooltip())
        )

    return mouseover
