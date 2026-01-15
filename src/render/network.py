import pygame
import math
from game_objects.level import Level
from game_objects.route import Route
from utils.image_loader import img_fetch
from render.constants import *


NETWORK_WIDTH = SCREEN_WIDTH - 20
NETWORK_HEIGHT = SCREEN_HEIGHT // 2

SCREEN_OFFSET = (10, 10)

ICON_SIZE = (60, 60)
ICON_HITBOX_SIZE = (50, 50)
VECTOR_SIZE = (40, 40)

VECTOR_FONT_SIZE = 32

color_map = {
    'PLAYER': pygame.Color('#51FC45'),
    'ENEMY': pygame.Color('#FF5555'),
    'NEUTRAL': pygame.Color('#DDDDDD'),
    'PLAYER_PATH': pygame.Color('#B1FFAB'),
    'ENEMY_PATH': pygame.Color('#FFB7B7')
}

WARD_COLOR = pygame.Color('#B8EAFF')
WARD_RADIUS = 35
WARD_FONT_SIZE = 26

DASHED_LINE_SEGMENT = 20  # Desired length
LINE_WIDTH = 3

VERTICAL_PATH_OFFSET = 4


def render_network(s: pygame.Surface, level: Level, routes: list[Route]=None):
    player_edges = []
    enemy_edges = []
    if routes:
        for route in routes:
            if route.owner == 'PLAYER':
                player_edges += route.edge_path
            elif route.owner == 'ENEMY':
                enemy_edges += route.edge_path

    # I don't understand why this requires pygame.SRCALPHA to be transparent and other surfaces don't
    network_surface = pygame.Surface((NETWORK_WIDTH, NETWORK_HEIGHT), pygame.SRCALPHA)

    x_cells = level.network_width
    y_cells = level.network_height

    cell_width = NETWORK_WIDTH // x_cells
    cell_height = NETWORK_HEIGHT // y_cells

    node_img = img_fetch().get('server-icon')
    node_img = pygame.transform.smoothscale(node_img, ICON_SIZE)

    interactables = {}

    for node_id, node in level.nodes.items():
        x_center = node.position[0]*cell_width + cell_width//2
        y_center = node.position[1]*cell_height + cell_height//2

        if len(node.right):
            for edge in node.right:
                next_node_x_center = edge.right.position[0]*cell_width + cell_width//2
                next_node_y_center = edge.right.position[1]*cell_height + cell_height//2

                # I don't know why the alpha gets messed up here and nowhere else
                c = color_map[edge.owner]
                c.a = 255
                draw_dashed_line(network_surface, c, LINE_WIDTH, (x_center, y_center), (next_node_x_center, next_node_y_center))

                # Draw planned routes
                if edge in player_edges:
                    pygame.draw.line(network_surface, color_map['PLAYER_PATH'], (x_center, y_center-VERTICAL_PATH_OFFSET),
                                     (next_node_x_center, next_node_y_center-VERTICAL_PATH_OFFSET), LINE_WIDTH)

                if edge in enemy_edges:
                    pygame.draw.line(network_surface, color_map['ENEMY_PATH'], (x_center, y_center+VERTICAL_PATH_OFFSET),
                                     (next_node_x_center, next_node_y_center+VERTICAL_PATH_OFFSET), LINE_WIDTH)

        network_surface.blit(recolor(node_img, color_map[node.owner]), (x_center-ICON_SIZE[0]//2, y_center-ICON_SIZE[1]//2))

        interactables[f'NODE{node_id}'] = pygame.Rect(SCREEN_OFFSET, ICON_HITBOX_SIZE)

        if node.vector:
            # Draw square container
            pygame.draw.rect(network_surface, color_map[node.owner], pygame.Rect(x_center-VECTOR_SIZE[0]//2, y_center-VECTOR_SIZE[1]//2, VECTOR_SIZE[0], VECTOR_SIZE[1]), width=2)

            # Draw vector text
            font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', VECTOR_FONT_SIZE)
            text = font.render(node.vector, True, color_map[node.owner])
            text_rect = text.get_rect(center=(x_center, y_center))
            network_surface.blit(text, text_rect)

        if node.ward:
            # Draw ward circle
            pygame.draw.circle(network_surface, WARD_COLOR, (x_center, y_center), WARD_RADIUS, width=2)

            # Draw ward value
            font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', WARD_FONT_SIZE)
            text = font.render(f'{node.ward}W', True, WARD_COLOR)
            text_rect = text.get_rect(center=(x_center, y_center+WARD_RADIUS))
            network_surface.blit(text, text_rect)

        # TODO: Draw something to identify source nodes

        # Render installed vectors

        s.blit(network_surface, SCREEN_OFFSET)

    return interactables


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