import pygame
from game_objects.card import Card
from utils.image_loader import img_fetch
from utils.text_helper import draw_text_with_outline
from constants import TERMINAL_GREEN, ENERGY_COLOR, DARK_TERMINAL


BORDER_COLOR = pygame.Color('#F5F2DA')  # Faded CRT tan
ENERGY_TEXT_COLOR = pygame.Color('#FFFFFF')
ENERGY_CENTER = (12, 12)
ENERGY_CIRCLE_RADIUS = 11
ENERGY_FONT_SIZE = 22
CARD_WIDTH = 140
CARD_HEIGHT = int(CARD_WIDTH * 1.4)
BORDER_WIDTH = 5
NAME_VERT_OFFSET = 14
NAME_FONT_SIZE = 16
NAME_FONT_SIZE_SMALL = 11
DESC_VERT_OFFSET = 120
DESC_LINE_OFFSET = 12
DESC_LEFT_OFFSET = 12
DESC_FONT_SIZE = 9
CARD_TYPE_BOX_SIZE = (100, 15)
IMAGE_VERT_OFFSET = 30
IMAGE_SIZE = (CARD_WIDTH-BORDER_WIDTH*2, 60)


def generate(card: Card):
    s = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))

    # Draw card back
    pygame.draw.rect(s, BORDER_COLOR, pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT), border_radius=5)
    pygame.draw.rect(s, DARK_TERMINAL, pygame.Rect(BORDER_WIDTH, BORDER_WIDTH, CARD_WIDTH-2*BORDER_WIDTH, CARD_HEIGHT-2*BORDER_WIDTH), border_radius=1)

    # Draw image
    image = img_fetch().get(card.image_id) or img_fetch().get('default')
    image = pygame.transform.smoothscale(image, IMAGE_SIZE)
    s.blit(image, (BORDER_WIDTH, IMAGE_VERT_OFFSET))

    # Draw title
    if len(card.name) <= 12:
        font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', NAME_FONT_SIZE)
    else:
        font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', NAME_FONT_SIZE_SMALL)
    outline_text = draw_text_with_outline(card.name, font, TERMINAL_GREEN, 2, 'black')
    text_rect = outline_text.get_rect(center=(CARD_WIDTH // 2, NAME_VERT_OFFSET))
    s.blit(outline_text, text_rect)

    # Draw card type
    pygame.draw.rect(s, BORDER_COLOR, pygame.Rect((CARD_WIDTH//2-CARD_TYPE_BOX_SIZE[0]//2, IMAGE_VERT_OFFSET+IMAGE_SIZE[1]), CARD_TYPE_BOX_SIZE), width=2)
    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', DESC_FONT_SIZE)
    text = font.render(card.type, True, TERMINAL_GREEN)
    text_rect = text.get_rect(center=(CARD_WIDTH//2, IMAGE_VERT_OFFSET+IMAGE_SIZE[1]+CARD_TYPE_BOX_SIZE[1]//2))
    s.blit(text, text_rect)

    # Draw description
    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', DESC_FONT_SIZE)
    if isinstance(card.description, list):
        for ndx, line in enumerate(card.description):
            text = font.render(line, True, TERMINAL_GREEN)
            text_rect = text.get_rect(topleft=(DESC_LEFT_OFFSET, DESC_VERT_OFFSET + ndx*DESC_LINE_OFFSET))
            s.blit(text, text_rect)
    else:
        text = font.render(card.description, True, TERMINAL_GREEN)
        text_rect = text.get_rect(topleft=(DESC_LEFT_OFFSET, DESC_VERT_OFFSET))
        s.blit(text, text_rect)

    # Draw energy
    pygame.draw.circle(s, ENERGY_COLOR, ENERGY_CENTER, ENERGY_CIRCLE_RADIUS)
    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', ENERGY_FONT_SIZE)
    outline_text = draw_text_with_outline(str(card.cost), font, ENERGY_TEXT_COLOR, 2, 'black')
    text_rect = outline_text.get_rect(center=ENERGY_CENTER)
    s.blit(outline_text, text_rect)

    return s


