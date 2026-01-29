import pygame
from game_objects.tag import Tag
from utils.image_loader import img_fetch
from utils.text_helper import draw_text_with_outline

TAG_ICON_SIZE = (12, 12)


def gen_tag(tag: Tag):
    s = pygame.Surface(TAG_ICON_SIZE)

    # TODO: Figure out why this displays with a black background despite being transparent
    image = img_fetch().get(tag.icon)
    image = pygame.transform.smoothscale(image, TAG_ICON_SIZE)
    s.blit(image, (0, 0))

    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', 8)
    outline_text = draw_text_with_outline(str(tag.count), font, 'white', 1, 'black')
    text_rect = outline_text.get_rect(center=(TAG_ICON_SIZE[0] - 4, TAG_ICON_SIZE[1] - 4))
    s.blit(outline_text, text_rect)

    return s