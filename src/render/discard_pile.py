import pygame
from game_objects.player import Player
from render.card import CARD_WIDTH, CARD_HEIGHT
from utils.image_loader import img_fetch


COUNT_OFFSET = (14, 14)
COUNT_RADIUS = 10
COUNT_FONT_SIZE = 20


def generate(player: Player):
    card_count = len(player.discard_pile)
    back = img_fetch().get('cardback')
    s = pygame.transform.smoothscale(back, (CARD_WIDTH//2, CARD_HEIGHT//2))

    pygame.draw.circle(s, 'red', COUNT_OFFSET, COUNT_RADIUS)
    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', COUNT_FONT_SIZE)
    text = font.render(str(card_count), True, 'white')
    text_rect = text.get_rect(center=COUNT_OFFSET)
    s.blit(text, text_rect)

    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', 14)
    text = font.render('Discard', True, 'white')
    text_rect = text.get_rect(center=(CARD_WIDTH//4, CARD_HEIGHT//4))
    s.blit(text, text_rect)

    return s