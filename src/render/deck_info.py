import pygame
from game_objects.player import Player
from render.card import CARD_WIDTH, CARD_HEIGHT
from utils.image_loader import img_fetch
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


TEXT_FONT_SIZE = 14
INFO_CARD_SIZE = (90, 126)


def render_deck_info(s: pygame.Surface, player: Player):
    back = img_fetch().get('cardback')
    card_surface = pygame.transform.smoothscale(back, INFO_CARD_SIZE)

    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', TEXT_FONT_SIZE)
    text = font.render(f'Draw: {len(player.draw_pile)}', True, 'white')
    text_rect = text.get_rect(center=(INFO_CARD_SIZE[0]//2, INFO_CARD_SIZE[1]//3))
    card_surface.blit(text, text_rect)

    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', TEXT_FONT_SIZE)
    text = font.render(f'Discard: {len(player.discard_pile)}', True, 'white')
    text_rect = text.get_rect(center=(INFO_CARD_SIZE[0]//2, INFO_CARD_SIZE[1]*2//3))
    card_surface.blit(text, text_rect)

    s.blit(card_surface, (SCREEN_WIDTH-200, SCREEN_HEIGHT-CARD_HEIGHT-10))

    # TODO: Interactables to give info on cards in draw and discard piles

    return {}
