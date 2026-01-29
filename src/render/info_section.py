from game_objects.player import Player
from game_objects.enemy import Enemy
from utils.image_loader import img_fetch
from constants import *


INFO_SECTION_SIZE = (120, 160)

PORTRAIT_SIZE = (100, 100)
PORTRAIT_VERT_OFFSET = 10

SCREEN_OFFSET_PLAYER = (30, 30)
SCREEN_OFFSET_ENEMY = (SCREEN_WIDTH - PORTRAIT_SIZE[0] - 30, 30)

HEALTH_FONT_SIZE = 24


def render_player_info(s: pygame.Surface, player: Player):
    info_surface = generate(player.portrait, player.health)
    s.blit(info_surface, SCREEN_OFFSET_PLAYER)

def render_enemy_info(s: pygame.Surface, enemy: Enemy):
    info_surface = generate(enemy.portrait, enemy.health)
    s.blit(info_surface, SCREEN_OFFSET_ENEMY)

def generate(portrait_id, health):
    s = pygame.Surface(INFO_SECTION_SIZE, pygame.SRCALPHA)
    offset = (INFO_SECTION_SIZE[0]//2 - PORTRAIT_SIZE[0]//2, PORTRAIT_VERT_OFFSET)

    # Draw portait and border
    img = img_fetch().get(portrait_id)
    img = pygame.transform.smoothscale(img, PORTRAIT_SIZE)
    s.blit(img, offset)
    pygame.draw.rect(s, '#444444', pygame.Rect(offset, PORTRAIT_SIZE), 5, 5)
    pygame.draw.rect(s, '#DDDDDD', pygame.Rect(offset, PORTRAIT_SIZE), 3, 5)

    # Draw health
    font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', HEALTH_FONT_SIZE)
    text = font.render(f'{health} HP', True, 'white')
    text_rect = text.get_rect(center=(INFO_SECTION_SIZE[0]//2, PORTRAIT_VERT_OFFSET+PORTRAIT_SIZE[1]+10))
    s.blit(text, text_rect)

    # TODO: Render tags

    return s
