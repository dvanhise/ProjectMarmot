import pygame
from game_objects.script import ScriptBuilder
from render.card import CARD_HEIGHT, CARD_WIDTH
from utils.image_loader import img_fetch
from render.constants import *


SCREEN_X_OFFSET = SCREEN_WIDTH // 2 - 250
SCREEN_Y_OFFSET = SCREEN_HEIGHT // 2 + 20

SPACING = 5
ARROW_WIDTH = 25
ARROW_HEIGHT = 10
HEADER_HEIGHT = 10

LABEL_FONT_SIZE = 24

BUTTON_SIZE = (100, 100)
BUTTON_FONT_SIZE = 20


def render_script_builder(s: pygame.Surface, builder: ScriptBuilder):
    interactables = {}
    current_x_offset = SCREEN_X_OFFSET
    # TODO: Account for multiple potential script types

    empty_img = img_fetch().get('empty-space')
    empty_img = pygame.transform.smoothscale(empty_img, (CARD_WIDTH, CARD_HEIGHT))

    arrow_img = img_fetch().get('arrow')
    arrow_img = pygame.transform.smoothscale(arrow_img, (ARROW_WIDTH, ARROW_HEIGHT))

    label_font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', LABEL_FONT_SIZE)

    # Draw payload spaces
    if not len(builder.payloads):
        s.blit(empty_img, (current_x_offset, SCREEN_Y_OFFSET))

        text = label_font.render('Payload', True, 'white')
        text_rect = text.get_rect(center=(current_x_offset + CARD_WIDTH // 2, SCREEN_Y_OFFSET + CARD_HEIGHT // 2))
        s.blit(text, text_rect)
    else:
        s.blit(builder.payloads[0], (0, 0))

    interactables['SCRIPT1'] = pygame.Rect(current_x_offset, SCREEN_Y_OFFSET, CARD_WIDTH, CARD_HEIGHT)

    current_x_offset += CARD_WIDTH + SPACING
    s.blit(arrow_img, (current_x_offset, SCREEN_Y_OFFSET + CARD_HEIGHT // 2))
    current_x_offset += ARROW_WIDTH + SPACING

    # Draw mod spaces
    if not len(builder.mods):
        s.blit(empty_img, (current_x_offset, SCREEN_Y_OFFSET))

        text = label_font.render('Mod', True, 'white')
        text_rect = text.get_rect(center=(current_x_offset + CARD_WIDTH // 2, SCREEN_Y_OFFSET + CARD_HEIGHT // 2))
        s.blit(text, text_rect)
    else:
        s.blit(builder.mods[0], (CARD_WIDTH+ARROW_WIDTH+2*SPACING, 0))

    interactables['SCRIPT2'] = pygame.Rect(current_x_offset, SCREEN_Y_OFFSET, CARD_WIDTH, CARD_HEIGHT)

    current_x_offset += CARD_WIDTH + SPACING
    s.blit(arrow_img, (current_x_offset, SCREEN_Y_OFFSET + CARD_HEIGHT // 2))
    current_x_offset += ARROW_WIDTH + SPACING

    # Draw vector spaces
    if not len(builder.vectors):
        s.blit(empty_img, (current_x_offset, SCREEN_Y_OFFSET))

        text = label_font.render('Vector', True, 'white')
        text_rect = text.get_rect(center=(current_x_offset + CARD_WIDTH // 2, SCREEN_Y_OFFSET + CARD_HEIGHT // 2))
        s.blit(text, text_rect)
    else:
        s.blit(builder.vectors[0], (CARD_WIDTH*2+ARROW_WIDTH*2+SPACING*4, 0))

    interactables['SCRIPT3'] = pygame.Rect(current_x_offset, SCREEN_Y_OFFSET, CARD_WIDTH, CARD_HEIGHT)

    current_x_offset += CARD_WIDTH + 40

    # Draw send script button
    image = img_fetch().get('button')
    image = pygame.transform.smoothscale(image, BUTTON_SIZE)
    s.blit(image, (current_x_offset, SCREEN_Y_OFFSET + CARD_HEIGHT//2 - BUTTON_SIZE[1]//2))

    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', BUTTON_FONT_SIZE)
    text = font.render('>>execute', True, 'white')
    text_rect = text.get_rect(center=(current_x_offset + BUTTON_SIZE[0]//2, SCREEN_Y_OFFSET + CARD_HEIGHT//2))
    s.blit(text, text_rect)

    interactables['SEND_SCRIPT'] = pygame.Rect((current_x_offset, SCREEN_Y_OFFSET + CARD_HEIGHT//2 - BUTTON_SIZE[1]//2), BUTTON_SIZE)

    return interactables