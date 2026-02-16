import pygame
from src.game_objects.card import Card
from src.utils.asset_loader import img_fetch, get_font
from src.utils.text_helper import draw_text_with_outline
from src.constants import TERMINAL_GREEN, ENERGY_COLOR, DARK_TERMINAL


BORDER_COLOR = pygame.Color('#F5F2DA')  # Faded CRT tan
ENERGY_TEXT_COLOR = pygame.Color('#FFFFFF')
ENERGY_CENTER = (12, 12)
ENERGY_CIRCLE_RADIUS = 11
ENERGY_FONT_SIZE = 22
CARD_WIDTH = 150
CARD_HEIGHT = int(CARD_WIDTH * 1.4)
BORDER_WIDTH = 5
NAME_VERT_OFFSET = 14
NAME_FONT_SIZE = 16
NAME_FONT_SIZE_SMALL = 11
DESC_VERT_OFFSET = 120
DESC_LINE_OFFSET = 12
DESC_LEFT_OFFSET = 12
DESC_FONT_SIZE = 10
CARD_TYPE_BOX_SIZE = (100, 15)
IMAGE_VERT_OFFSET = 30
IMAGE_BORDER_OVERLAP = 3
IMAGE_SIZE = (CARD_WIDTH-BORDER_WIDTH*2+IMAGE_BORDER_OVERLAP*2, 60)

RARITY_COLOR_MAP = {
    'built-in': '#AAAAAA',
    'simple': '#ACF55F',
    'intermediate': '#ABFAFF',
    'elite': '#FFFB14',
    'special': '#444444'
}


def gen_card(card: Card):
    s = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))

    # Draw card back
    pygame.draw.rect(s, BORDER_COLOR, pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT), border_radius=5)
    pygame.draw.rect(s, DARK_TERMINAL, pygame.Rect(BORDER_WIDTH, BORDER_WIDTH, CARD_WIDTH-2*BORDER_WIDTH, CARD_HEIGHT-2*BORDER_WIDTH), border_radius=1)

    # Draw image
    image = img_fetch().get(card.image_id) or img_fetch().get('default')
    image = pygame.transform.smoothscale(image, IMAGE_SIZE)
    s.blit(image, (BORDER_WIDTH-IMAGE_BORDER_OVERLAP, IMAGE_VERT_OFFSET))

    # Draw rarity color on border
    pygame.draw.rect(s, RARITY_COLOR_MAP[card.rarity], pygame.Rect((BORDER_WIDTH-IMAGE_BORDER_OVERLAP, IMAGE_VERT_OFFSET), IMAGE_SIZE), width=4)

    # Draw title
    if len(card.name) <= 12:
        font = pygame.font.Font(get_font('BrassMono', 'bold'), NAME_FONT_SIZE)
    else:
        font = pygame.font.Font(get_font('BrassMono', 'bold'), NAME_FONT_SIZE_SMALL)
    outline_text = draw_text_with_outline(card.name, font, TERMINAL_GREEN, 2, 'black')
    text_rect = outline_text.get_rect(center=(CARD_WIDTH // 2, NAME_VERT_OFFSET))
    s.blit(outline_text, text_rect)

    # Draw card type
    pygame.draw.rect(s, BORDER_COLOR, pygame.Rect((CARD_WIDTH//2-CARD_TYPE_BOX_SIZE[0]//2, IMAGE_VERT_OFFSET+IMAGE_SIZE[1]), CARD_TYPE_BOX_SIZE), width=2)
    font = pygame.font.Font(get_font('BrassMono', 'regular'), DESC_FONT_SIZE)
    text = font.render(card.type, True, TERMINAL_GREEN)
    text_rect = text.get_rect(center=(CARD_WIDTH//2, IMAGE_VERT_OFFSET+IMAGE_SIZE[1]+CARD_TYPE_BOX_SIZE[1]//2))
    s.blit(text, text_rect)

    # Draw description
    font = pygame.font.Font(get_font('BrassMono', 'regular'), DESC_FONT_SIZE)
    for ndx, line in enumerate(card.get_description()):
        text = font.render(line, True, TERMINAL_GREEN)
        text_rect = text.get_rect(topleft=(DESC_LEFT_OFFSET, DESC_VERT_OFFSET + ndx*DESC_LINE_OFFSET))
        s.blit(text, text_rect)

    # Draw energy
    pygame.draw.circle(s, ENERGY_COLOR, ENERGY_CENTER, ENERGY_CIRCLE_RADIUS)
    font = pygame.font.Font(get_font('BrassMono', 'bold'), ENERGY_FONT_SIZE)
    outline_text = draw_text_with_outline(str(card.cost), font, ENERGY_TEXT_COLOR, 2, 'black')
    text_rect = outline_text.get_rect(center=ENERGY_CENTER)
    s.blit(outline_text, text_rect)

    return s


# Meta card render for health gain option at round end
def gen_health_card(value):
    s = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))

    # Draw card back
    pygame.draw.rect(s, BORDER_COLOR, pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT), border_radius=5)
    pygame.draw.rect(s, DARK_TERMINAL, pygame.Rect(BORDER_WIDTH, BORDER_WIDTH, CARD_WIDTH-2*BORDER_WIDTH, CARD_HEIGHT-2*BORDER_WIDTH), border_radius=1)

    font = pygame.font.Font(get_font('BrassMono', 'regular'), 26)
    outline_text = draw_text_with_outline(f'+{value} HP', font, 'white', 2, 'black')
    text_rect = outline_text.get_rect( center=(CARD_WIDTH//2, CARD_HEIGHT//2))
    s.blit(outline_text, text_rect)

    return s



