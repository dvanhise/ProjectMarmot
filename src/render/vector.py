import pygame
from game_objects.vector import Vector
from render.tag import gen_tag, TAG_ICON_SIZE
from utils.mouse_check import Tooltip
from constants import DARK_TERMINAL

VECTOR_WIDTH = 26
VECTOR_FONT_SIZE = 11
VECTOR_NAME_OFFSET = 10
PADDING = 1

def render_vector(s: pygame.Surface, left, top, vector: Vector, color: pygame.Color):
    calculated_height = max(len(vector.tags), 1)*TAG_ICON_SIZE[1]+VECTOR_NAME_OFFSET+3*PADDING
    mouseover = []

    # Draw square container and border
    pygame.draw.rect(s, DARK_TERMINAL, pygame.Rect(left, top, VECTOR_WIDTH, calculated_height))
    pygame.draw.rect(s, 'white', pygame.Rect(left, top, VECTOR_WIDTH, calculated_height), width=1)

    # Draw title
    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', VECTOR_FONT_SIZE)
    text = font.render(vector.name, True, 'white')
    text_rect = text.get_rect(center=(left+VECTOR_WIDTH//2, top+PADDING+4))
    s.blit(text, text_rect)

    for ndx, tag in enumerate(vector.tags):
        s.blit(gen_tag(tag), (left+VECTOR_WIDTH//2-TAG_ICON_SIZE[0]//2, top+PADDING*2+VECTOR_NAME_OFFSET+ndx*TAG_ICON_SIZE[1]))
        mouseover.append(
            Tooltip(pygame.Rect((left+VECTOR_WIDTH//2-TAG_ICON_SIZE[0]//2, top+VECTOR_NAME_OFFSET+ndx*TAG_ICON_SIZE[1]), TAG_ICON_SIZE),
                    tag.get_tooltip())
        )

    return mouseover
