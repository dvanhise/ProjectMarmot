import pygame
from game_objects.card import Card
from utils.image_loader import img_fetch


BG_COLOR = pygame.Color('#282828')  # Dark screen
BORDER_COLOR = pygame.Color('#F5F2DA')  # Faded CRT tan
TEXT_COLOR = pygame.Color('#33FF33')  # CRT green
ENERGY_CIRCLE_COLOR = pygame.Color('#1E2888')  # Blueish
ENERGY_COLOR = pygame.Color('#FFFFFF')
ENERGY_CENTER = (12, 12)
ENERGY_CIRCLE_RADIUS = 10
ENERGY_FONT_SIZE = 30
CARD_WIDTH = 120
CARD_HEIGHT = int(CARD_WIDTH * 1.4)
BORDER_WIDTH = 5
NAME_VERT_OFFSET = 14
NAME_FONT_SIZE = 24
DESCRIPTION_VERT_OFFSET = 90
DESCRIPTION_FONT_SIZE = 14
IMAGE_VERT_OFFSET = 30
IMAGE_SIZE = (CARD_WIDTH-BORDER_WIDTH*2, 50)


def generate(card: Card):
    s = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))

    # Draw card back
    pygame.draw.rect(s, BORDER_COLOR, pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT), border_radius=5)
    pygame.draw.rect(s, BG_COLOR, pygame.Rect(BORDER_WIDTH, BORDER_WIDTH, CARD_WIDTH-2*BORDER_WIDTH, CARD_HEIGHT-2*BORDER_WIDTH), border_radius=1)

    # Draw image
    image = img_fetch().get(card.image_id) or img_fetch().get('default')
    image = pygame.transform.smoothscale(image, IMAGE_SIZE)
    s.blit(image, (BORDER_WIDTH, IMAGE_VERT_OFFSET))

    # Draw title
    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', NAME_FONT_SIZE)
    text = font.render(card.name, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(CARD_WIDTH//2, NAME_VERT_OFFSET))
    s.blit(text, text_rect)

    # Draw description
    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', DESCRIPTION_FONT_SIZE)
    text = font.render(card.description, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(CARD_WIDTH//2, DESCRIPTION_VERT_OFFSET))
    s.blit(text, text_rect)

    # Draw energy
    pygame.draw.circle(s, ENERGY_CIRCLE_COLOR, ENERGY_CENTER, ENERGY_CIRCLE_RADIUS)
    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', ENERGY_FONT_SIZE)
    text = font.render(str(card.cost), True, ENERGY_COLOR)
    text_rect = text.get_rect(center=ENERGY_CENTER)
    s.blit(text, text_rect)

    return s