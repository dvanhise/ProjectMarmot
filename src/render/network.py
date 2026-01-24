import pygame
import math
from game_objects.level import Level
from game_objects.route import Route
from game_objects.script import Script
from render.vector import generate as gen_vector
from utils.image_loader import img_fetch
from utils.text_helper import draw_text_with_outline
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


NETWORK_WIDTH = SCREEN_WIDTH
NETWORK_HEIGHT = SCREEN_HEIGHT // 2

SCREEN_OFFSET = (0, 0)

ICON_SIZE = (60, 60)
ICON_HITBOX_SIZE = (50, 50)
VECTOR_SIZE = (32, 32)

VECTOR_FONT_SIZE = 14

INSTALL_VECTOR_OFFSET = 40
INSTALL_VECTOR_BORDER = 5

SCRIPT_POWER_SIZE = (50, 50)
SCRIPT_X_OFFSET = 10
SCRIPT_Y_OFFSET = -10

color_map = {
    'PLAYER': pygame.Color('#51FC45'),
    'ENEMY': pygame.Color('#FF5555'),
    'NEUTRAL': pygame.Color('#DDDDDD'),
    'PLAYER_PATH': pygame.Color('#51FC45'),
    'ENEMY_PATH': pygame.Color('#FF5555')
}

WARD_COLOR = pygame.Color('#B8EAFF')
WARD_RADIUS = 35
WARD_FONT_SIZE = 18

SELECTABLE_NODE_RADIUS = 50
SELECTABLE_NODE_COLOR = pygame.Color('#FFFFFF')

DASHED_LINE_SEGMENT = 20  # Desired length
LINE_WIDTH = 3

VERTICAL_PATH_OFFSET = 5


def render_network(s: pygame.Surface, level: Level, script: Script, routes: list[Route]=None):
    player_edges = []
    enemy_edges = []
    player_route = None
    for route in [r for r in routes if r] if routes else []:
        if route.owner == 'PLAYER':
            player_route = route
            player_edges += route.edge_path
        elif route.owner == 'ENEMY':
            enemy_edges += route.edge_path

    node_choices = player_route.get_next_node_options() if player_route else []
    edge_choices = player_route.get_next_edge_options() if player_route else []

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

                # Draw route choices
                if edge in edge_choices:
                    draw_dashed_line(network_surface, c, LINE_WIDTH+2, (x_center, y_center),(next_node_x_center, next_node_y_center))

        network_surface.blit(recolor(node_img, color_map[node.owner]), (x_center-ICON_SIZE[0]//2, y_center-ICON_SIZE[1]//2))

        # Draw selectable node identification circles
        if node in node_choices:
            # FIXME: issues with colors from color_map being transparent
            pygame.draw.circle(network_surface, SELECTABLE_NODE_COLOR, (x_center, y_center), SELECTABLE_NODE_RADIUS, width=5)
            pygame.draw.circle(network_surface, pygame.Color('#51FC45'), (x_center, y_center), SELECTABLE_NODE_RADIUS, width=2)

        interactables[f'NODE{node_id}'] = pygame.Rect((SCREEN_OFFSET[0]+x_center-ICON_HITBOX_SIZE[0]//2, SCREEN_OFFSET[1]+y_center-ICON_HITBOX_SIZE[1]//2), ICON_HITBOX_SIZE)

        # Add info on the script and vector installation for the current node
        if player_route and node == player_route.node_path[-1]:
            installable_vector_count = len(script.vector)
            if installable_vector_count:
                box_width = installable_vector_count*(INSTALL_VECTOR_BORDER+1)+VECTOR_SIZE[0]+3
                box_height = VECTOR_SIZE[1]+INSTALL_VECTOR_BORDER*2
                box_left = x_center-box_width//2
                box_top = y_center+INSTALL_VECTOR_OFFSET

                pygame.draw.rect(network_surface, 'blue', pygame.Rect((box_left, box_top),(box_width, box_height)))
                for ndx, vector in enumerate(script.vector):
                    vector_render = gen_vector(vector, pygame.Color('#51FC45'))
                    network_surface.blit(vector_render, (box_left+ndx*VECTOR_SIZE[0]+(ndx+1)*INSTALL_VECTOR_BORDER, box_top+INSTALL_VECTOR_BORDER))
                    interactables[f'INSTALL_VECTOR{ndx}'] = pygame.Rect((box_left+ndx*VECTOR_SIZE[0]+(ndx+1)*INSTALL_VECTOR_BORDER, box_top+INSTALL_VECTOR_BORDER), VECTOR_SIZE)

                # Add help text above vector box
                action_text = 'Overwrite Vector?' if node.vector else 'Install Vector?'
                font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', 14)
                text = font.render(action_text, True, 'white')
                text_rect = text.get_rect(center=(x_center, box_top+VECTOR_SIZE[1]+20))
                network_surface.blit(text, text_rect)

            # Draw info on the executing script
            script_img = img_fetch().get('power')
            script_img = pygame.transform.smoothscale(script_img, SCRIPT_POWER_SIZE)
            network_surface.blit(script_img, (x_center+SCRIPT_X_OFFSET, y_center+SCRIPT_Y_OFFSET))

            font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', 24)
            power_text = draw_text_with_outline(str(script.power), font, 'white', 1, 'black')
            text_rect = power_text.get_rect(center=(x_center+SCRIPT_X_OFFSET+SCRIPT_POWER_SIZE[0]//2, y_center+SCRIPT_Y_OFFSET+SCRIPT_POWER_SIZE[1]//2))
            network_surface.blit(power_text, text_rect)

        if node.vector:
            # Draw square container
            pygame.draw.rect(network_surface, 'black', pygame.Rect(x_center-VECTOR_SIZE[0]//2, y_center-VECTOR_SIZE[1]//2, VECTOR_SIZE[0], VECTOR_SIZE[1]))

            # Draw border
            c = color_map[node.owner]
            c.a = 255
            pygame.draw.rect(network_surface, c, pygame.Rect(x_center-VECTOR_SIZE[0]//2, y_center-VECTOR_SIZE[1]//2, VECTOR_SIZE[0], VECTOR_SIZE[1]), width=2)

            # Draw vector text
            font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', VECTOR_FONT_SIZE)
            text = font.render(f'P+{node.vector.power_boost}', True, color_map[node.owner])
            text_rect = text.get_rect(center=(x_center, y_center))
            network_surface.blit(text, text_rect)

        if node.ward:
            # Draw ward circle
            pygame.draw.circle(network_surface, WARD_COLOR, (x_center, y_center), WARD_RADIUS, width=2)

            # Draw ward value
            font = pygame.font.Font('assets/fonts/BrassMono-Bold.ttf', WARD_FONT_SIZE)
            text = font.render(f'{node.ward}W', True, WARD_COLOR)
            text_rect = text.get_rect(center=(x_center, y_center+WARD_RADIUS + 6))
            network_surface.blit(text, text_rect)

        # TODO: Render installed vectors

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