import pygame
import math
from game_objects.level import Level
from utils.image_loader import img_fetch
from render.constants import *


BOARD_WIDTH = SCREEN_WIDTH - 20
BOARD_HEIGHT = SCREEN_HEIGHT // 2

ICON_SIZE = (50, 50)
VECTOR_SIZE = (30, 30)

VECTOR_FONT_SIZE = 32

color_map = {
    'PLAYER': pygame.Color('#51FC45'),
    'ENEMY': pygame.Color('#FF5555'),
    'NEUTRAL': pygame.Color('#DDDDDD')
}

WARD_COLOR = pygame.Color('#B8EAFF')
WARD_RADIUS = 30
WARD_FONT_SIZE = 24

DASHED_LINE_SEGMENT = 20  # Desired length
DASHED_LINE_WIDTH = 3


def generate(level: Level):
    s = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))

    x_cells = level.board_width
    y_cells = level.board_height

    cell_width = BOARD_WIDTH // x_cells
    cell_height = BOARD_HEIGHT // y_cells

    node_img = img_fetch().get('server-icon')
    node_img = pygame.transform.smoothscale(node_img, ICON_SIZE)

    for node in level.nodes.values():
        x_center = node.position[0]*cell_width + cell_width//2
        y_center = node.position[1]*cell_height + cell_height//2

        if len(node.right):
            for edge in node.right:
                next_node_x_center = edge.right.position[0]*cell_width + cell_width//2
                next_node_y_center = edge.right.position[1]*cell_height + cell_height//2

                draw_dashed_line(s, color_map[edge.owner], DASHED_LINE_WIDTH, (x_center, y_center), (next_node_x_center, next_node_y_center))

        s.blit(recolor(node_img, color_map[node.owner]), (x_center-ICON_SIZE[0]//2, y_center-ICON_SIZE[1]//2))

        if node.vector:
            # Draw square container
            pygame.draw.rect(s, color_map[node.owner], pygame.Rect(x_center-VECTOR_SIZE[0]//2, y_center-VECTOR_SIZE[1]//2, VECTOR_SIZE[0], VECTOR_SIZE[1]), width=2)

            # Draw vector text
            font = pygame.font.Font(None, VECTOR_FONT_SIZE)
            text = font.render(node.vector, True, color_map[node.owner])
            text_rect = text.get_rect(center=(x_center, y_center))
            s.blit(text, text_rect)

        if node.ward:
            # Draw ward circle
            pygame.draw.circle(s, WARD_COLOR, (x_center, y_center), WARD_RADIUS, width=1)

            # Draw ward value
            font = pygame.font.Font(None, WARD_FONT_SIZE)
            text = font.render(f'{node.ward}🛡️', True, WARD_COLOR)
            text_rect = text.get_rect(center=(x_center, y_center+WARD_RADIUS))
            s.blit(text, text_rect)



    return s


def recolor(surface: pygame.Surface, color: pygame.Color):
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            color.a = surface.get_at((x, y))[3]
            surface.set_at((x, y), color)

    return surface

def draw_dashed_line(surface: pygame.Surface, color: pygame.Color, width, start_pos, end_pos):
    x_diff = end_pos[0]-start_pos[0]
    y_diff = end_pos[1]-start_pos[1]
    total_length = int(math.sqrt(x_diff**2 + y_diff**2))
    segments = round(total_length/DASHED_LINE_SEGMENT)
    x_segment_diff = x_diff // segments
    y_segment_diff = y_diff // segments
    for i in range(segments):
        if i % 2 == 1:
            continue
        pygame.draw.line(
            surface,
            color,
            (start_pos[0]+i*x_segment_diff, start_pos[1]+i*y_segment_diff),
            (start_pos[0]+(i+1)*x_segment_diff, start_pos[1]+(i+1)*y_segment_diff),
            width=width)