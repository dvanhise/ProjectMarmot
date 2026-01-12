import pygame
from game_objects.script import ScriptBuilder
from render.card import CARD_HEIGHT, CARD_WIDTH
from utils.image_loader import img_fetch


SPACING = 3
ARROW_WIDTH = 15
HEADER_HEIGHT = 10


def generate(builder: ScriptBuilder):
    s = pygame.Surface((CARD_WIDTH*3+ARROW_WIDTH*2+SPACING*4, CARD_HEIGHT))

    empty_img = img_fetch().get('empty-space')
    empty_img = pygame.transform.smoothscale(empty_img, (CARD_WIDTH, CARD_HEIGHT))

    # Draw payload space
    if not len(builder.payloads):
        s.blit(empty_img, (0, 0))
    else:
        s.blit(builder.payloads[0], (0, 0))

    # Draw mod space
    if not len(builder.mods):
        s.blit(empty_img, (CARD_WIDTH+ARROW_WIDTH+2*SPACING, 0))
    else:
        s.blit(builder.mods[0], (CARD_WIDTH+ARROW_WIDTH+2*SPACING, 0))

    # Draw vector space
    if not len(builder.vectors):
        s.blit(empty_img, (CARD_WIDTH*2+ARROW_WIDTH*2+SPACING*4, 0))
    else:
        s.blit(builder.vectors[0], (CARD_WIDTH*2+ARROW_WIDTH*2+SPACING*4, 0))

    # TODO: Draw arrows

    return s