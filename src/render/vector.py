import pygame
from game_objects.vector import Vector

VECTOR_SIZE = (32, 32)
VECTOR_FONT_SIZE = 14

def generate(vector: Vector, color: pygame.Color):
    s = pygame.Surface(VECTOR_SIZE)

    # Draw square container
    pygame.draw.rect(s, 'black', pygame.Rect(0, 0, VECTOR_SIZE[0], VECTOR_SIZE[1]))

    # Drew border
    pygame.draw.rect(s, color, pygame.Rect(0, 0, VECTOR_SIZE[0], VECTOR_SIZE[1]), width=2)

    # Draw vector text
    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', VECTOR_FONT_SIZE)
    text = font.render(f'P+{vector.power_boost}', True, color)
    text_rect = text.get_rect(center=(VECTOR_SIZE[0]//2, VECTOR_SIZE[1]//2))
    s.blit(text, text_rect)

    return s
