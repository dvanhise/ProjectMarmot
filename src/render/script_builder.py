import pygame
from src.game_objects.script import ScriptBuilder
from src.game_objects.card_type import CardType
from src.render.card import CARD_HEIGHT, CARD_WIDTH, gen_card
from src.render.network import NETWORK_HEIGHT
from src.utils.asset_loader import img_fetch, get_font
from src.utils.text_helper import draw_text_with_outline
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, ENERGY_COLOR


SCREEN_Y_OFFSET = NETWORK_HEIGHT + 10
RIGHT_OFFSET = 180

SPACING = 2
ARROW_WIDTH = 25
ARROW_HEIGHT = 22
HEADER_HEIGHT = 10

LABEL_FONT_SIZE = 24

BUTTON_SIZE = (150, 110)

LABEL_MAP = {
    CardType.SCRIPT_PAYLOAD: 'Payload',
    CardType.SCRIPT_MOD: 'Mod',
    CardType.SCRIPT_VECTOR: 'Vector'
}


def render_script_builder(s: pygame.Surface, builder: ScriptBuilder):
    interactables = {}
    slots = len(builder.slots)
    current_x_offset = SCREEN_WIDTH - RIGHT_OFFSET - slots*(CARD_WIDTH+ARROW_WIDTH)

    empty_img = img_fetch().get('empty-space')
    empty_img = pygame.transform.smoothscale(empty_img, (CARD_WIDTH, CARD_HEIGHT))

    arrow_img = img_fetch().get('arrow')
    arrow_img = pygame.transform.smoothscale(arrow_img, (ARROW_WIDTH, ARROW_HEIGHT))

    label_font = pygame.font.Font(get_font('BrassMono', 'regular'), LABEL_FONT_SIZE)

    for ndx, slot in enumerate(builder.slots):
        if not slot.card:
            s.blit(empty_img, (current_x_offset, SCREEN_Y_OFFSET))

            text = label_font.render(LABEL_MAP[slot.type], True, 'white')
            text_rect = text.get_rect(center=(current_x_offset + CARD_WIDTH // 2, SCREEN_Y_OFFSET + CARD_HEIGHT // 2))
            s.blit(text, text_rect)
        else:
            s.blit(gen_card(slot.card), (current_x_offset, SCREEN_Y_OFFSET))

        interactables[f'SCRIPT{ndx}'] = pygame.Rect(current_x_offset, SCREEN_Y_OFFSET, CARD_WIDTH, CARD_HEIGHT)

        current_x_offset += CARD_WIDTH + SPACING

        s.blit(arrow_img, (current_x_offset, SCREEN_Y_OFFSET + CARD_HEIGHT // 2 - 10))
        current_x_offset += ARROW_WIDTH + SPACING

    current_x_offset += CARD_WIDTH + 40

    # Draw send script button
    image = img_fetch().get('execute')
    image = pygame.transform.smoothscale(image, BUTTON_SIZE)
    s.blit(image, (SCREEN_WIDTH-BUTTON_SIZE[0]-12, SCREEN_Y_OFFSET + CARD_HEIGHT//2 - BUTTON_SIZE[1]//2))

    # Add energy cost to button
    pygame.draw.circle(s, ENERGY_COLOR, (SCREEN_WIDTH-BUTTON_SIZE[0]+45, SCREEN_Y_OFFSET+62), 16)
    font = pygame.font.Font(get_font('BrassMono', 'bold'), 26)
    outline_text = draw_text_with_outline('1', font, 'white', 2, 'black')
    text_rect = outline_text.get_rect(center=(SCREEN_WIDTH - BUTTON_SIZE[0]+45, SCREEN_Y_OFFSET+62))
    s.blit(outline_text, text_rect)

    interactables['SEND_SCRIPT'] = pygame.Rect((SCREEN_WIDTH-BUTTON_SIZE[0]-10, SCREEN_Y_OFFSET + CARD_HEIGHT//2 - BUTTON_SIZE[1]//2), BUTTON_SIZE)

    return interactables