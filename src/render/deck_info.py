import pygame
from src.game_objects.player import Player
from src.game_objects.deck_category import DeckCategory
from src.render.card import CARD_WIDTH, CARD_HEIGHT
from src.utils.asset_loader import img_fetch, get_font
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


TEXT_FONT_SIZE = 13
INFO_CARD_SIZE = (90, 126)

VERT_OFFSET = 25


def render_deck_info(s: pygame.Surface,  player: Player):
    left = SCREEN_WIDTH-INFO_CARD_SIZE[0]-10
    top = SCREEN_HEIGHT-CARD_HEIGHT-10

    back = img_fetch().get('cardback')
    card_surface = pygame.transform.smoothscale(back, INFO_CARD_SIZE)
    s.blit(card_surface, (left, top))

    interactables = {}

    font = pygame.font.Font(get_font('BrassMono', 'bold'), TEXT_FONT_SIZE)

    text = font.render(f'Full Deck: {len(player.all_cards)}', True, 'white')
    text_rect = text.get_rect(center=(left+INFO_CARD_SIZE[0]//2, top+VERT_OFFSET))
    s.blit(text, text_rect)
    interactables[f'VIEW_DECK{DeckCategory.FULL}'] = text_rect

    text = font.render(f'Draw: {len(player.draw_pile)}', True, 'white')
    text_rect = text.get_rect(center=(left+INFO_CARD_SIZE[0]//2, top+VERT_OFFSET*2))
    s.blit(text, text_rect)
    interactables[f'VIEW_DECK{DeckCategory.DRAW}'] = text_rect

    text = font.render(f'Discard: {len(player.discard_pile)}', True, 'white')
    text_rect = text.get_rect(center=(left+INFO_CARD_SIZE[0]//2, top+VERT_OFFSET*3))
    s.blit(text, text_rect)
    interactables[f'VIEW_DECK{DeckCategory.DISCARD}'] = text_rect

    text = font.render(f'Deleted: {len(player.deleted_pile)}', True, 'white')
    text_rect = text.get_rect(center=(left+INFO_CARD_SIZE[0]//2, top+VERT_OFFSET*4))
    s.blit(text, text_rect)
    interactables[f'VIEW_DECK{DeckCategory.DELETED}'] = text_rect

    return interactables
