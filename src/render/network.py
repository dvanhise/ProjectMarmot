import pygame
import math
from src.game_objects.level import Level
from src.game_objects.route import Route
from src.game_objects.script import Script
from src.render.vector import render_vector, VECTOR_WIDTH
from src.render.tag import gen_tag, TAG_ICON_SIZE
from src.utils.asset_loader import img_fetch, get_font
from src.utils.mouse_check import Tooltip
from src.utils.text_helper import draw_text_with_outline
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


NETWORK_WIDTH = SCREEN_WIDTH
NETWORK_HEIGHT = SCREEN_HEIGHT // 2 + 20

ICON_SIZE = (70, 70)
ICON_HITBOX_SIZE = (60, 60)
VECTOR_SIZE = (32, 32)

INSTALL_VECTOR_OFFSET = 40
INSTALL_VECTOR_BORDER = 5

SCRIPT_POWER_SIZE = (50, 50)
SCRIPT_X_OFFSET = 10
SCRIPT_Y_OFFSET = -10

ENEMY_SCRIPT_X_OFFSET = -10
ENEMY_SCRIPT_Y_OFFSET = -10

color_map = {
    'PLAYER': pygame.Color('#51FC45'),
    'ENEMY': pygame.Color('#FF5555'),
    'NEUTRAL': pygame.Color('#DDDDDD'),
    'PLAYER_PATH': pygame.Color('#51FC45'),
    'ENEMY_PATH': pygame.Color('#FF5555')
}

WARD_COLOR = pygame.Color('#B8EAFF')
WARD_RADIUS = 42
WARD_FONT_SIZE = 18

SELECTABLE_NODE_RADIUS = 50
SELECTABLE_NODE_COLOR = pygame.Color('#FFFFFF')

DASHED_LINE_SEGMENT = 20  # Desired length
LINE_WIDTH = 3
EDGE_DEGREDATION_RADIUS = 9

VERTICAL_PATH_OFFSET = 5

VERTICAL_PADDING = 15


def render_network(s: pygame.Surface, level: Level, script: Script, enemy_script: Script, routes: list[Route]=None):
    player_edges = []
    enemy_edges = []
    player_route = None
    enemy_route = None
    for route in [r for r in routes if r] if routes else []:
        if route.owner == 'PLAYER':
            player_route = route
            player_edges += route.edge_path
        elif route.owner == 'ENEMY':
            enemy_route = route
            enemy_edges += route.edge_path

    node_choices = player_route.get_next_node_options() if player_route else []
    edge_choices = player_route.get_next_edge_options() if player_route else []

    # I don't understand why this requires pygame.SRCALPHA to be transparent and other surfaces don't
    # s = pygame.Surface((NETWORK_WIDTH, NETWORK_HEIGHT), pygame.SRCALPHA)

    x_cells = level.network_width
    y_cells = level.network_height

    cell_width = NETWORK_WIDTH // x_cells
    cell_height = (NETWORK_HEIGHT-VERTICAL_PADDING*2) // y_cells

    node_img = img_fetch().get('server-icon')
    node_img = pygame.transform.smoothscale(node_img, ICON_SIZE)
    script_img = img_fetch().get('power')
    script_img = pygame.transform.smoothscale(script_img, SCRIPT_POWER_SIZE)

    interactables = {}
    mouseovers = []

    for node_id, node in level.nodes.items():
        x_center = node.position[0]*cell_width + cell_width//2
        y_center = node.position[1]*cell_height + cell_height//2 + VERTICAL_PADDING

        if len(node.right):
            for edge in node.right:
                next_node_x_center = edge.right.position[0]*cell_width + cell_width//2
                next_node_y_center = edge.right.position[1]*cell_height + cell_height//2

                # Draw edges
                # I don't know why the alpha gets messed up here and nowhere else
                c = color_map[edge.owner]
                c.a = 255
                draw_dashed_line(s, c, LINE_WIDTH, (x_center, y_center), (next_node_x_center, next_node_y_center))

                # Add edge script degredation
                midpoint_x = (x_center+next_node_x_center)//2
                midpoint_y = (y_center+next_node_y_center)//2
                pygame.draw.circle(s, c, (midpoint_x, midpoint_y), EDGE_DEGREDATION_RADIUS)
                font = pygame.font.Font(get_font('BrassMono', 'bold'), 16)
                text = font.render(str(edge.difficulty), True, 'black')
                text_rect = text.get_rect(center=(midpoint_x, midpoint_y))
                s.blit(text, text_rect)
                mouseovers.append(Tooltip(pygame.Rect(
                    midpoint_x-EDGE_DEGREDATION_RADIUS//2,
                    midpoint_y-EDGE_DEGREDATION_RADIUS//2,
                    EDGE_DEGREDATION_RADIUS,
                    EDGE_DEGREDATION_RADIUS
                ), f'Edge penalty: Reduces power of non-friendly scripts by {edge.difficulty}.'))

                # Draw planned routes
                if edge in player_edges:
                    pygame.draw.line(s, color_map['PLAYER_PATH'], (x_center, y_center-VERTICAL_PATH_OFFSET),
                                     (next_node_x_center, next_node_y_center-VERTICAL_PATH_OFFSET), LINE_WIDTH)

                if edge in enemy_edges:
                    pygame.draw.line(s, color_map['ENEMY_PATH'], (x_center, y_center+VERTICAL_PATH_OFFSET),
                                     (next_node_x_center, next_node_y_center+VERTICAL_PATH_OFFSET), LINE_WIDTH)

                # Draw route choices
                if edge in edge_choices:
                    draw_dashed_line(s, c, LINE_WIDTH+2, (x_center, y_center),(next_node_x_center, next_node_y_center))

        # Draw node image
        s.blit(recolor(node_img, color_map[node.owner]), (x_center-ICON_SIZE[0]//2, y_center-ICON_SIZE[1]//2))

        # Draw node tags
        width = len(node.tags)*TAG_ICON_SIZE[0]
        tag_left_offset = x_center - width//2
        tag_top_offset = y_center - ICON_SIZE[1]//2-10
        for ndx, tag in enumerate(node.tags):
            s.blit(gen_tag(tag), (tag_left_offset+ndx*TAG_ICON_SIZE[0], tag_top_offset))

            mouseovers.append(Tooltip(
                pygame.Rect((tag_left_offset+ndx*TAG_ICON_SIZE[0], tag_top_offset), TAG_ICON_SIZE),
                tag.get_tooltip()
            ))

        # Draw selectable node identification circles
        if node in node_choices:
            # FIXME: issues with colors from color_map being transparent
            pygame.draw.circle(s, SELECTABLE_NODE_COLOR, (x_center, y_center), SELECTABLE_NODE_RADIUS, width=5)
            pygame.draw.circle(s, pygame.Color('#51FC45'), (x_center, y_center), SELECTABLE_NODE_RADIUS, width=2)

        interactables[f'NODE{node_id}'] = pygame.Rect((x_center-ICON_HITBOX_SIZE[0]//2, y_center-ICON_HITBOX_SIZE[1]//2), ICON_HITBOX_SIZE)

        if node.vector:
            c = color_map[node.owner]
            c.a = 255
            new_mouseovers = render_vector(s,
               x_center-VECTOR_WIDTH//2,
               y_center-VECTOR_SIZE[1]//2,
               node.vector, c)
            mouseovers += new_mouseovers

        if node.ward:
            # Draw ward circle
            pygame.draw.circle(s, WARD_COLOR, (x_center, y_center), WARD_RADIUS, width=2)

            # Draw ward value
            font = pygame.font.Font(get_font('BrassMono', 'bold'), WARD_FONT_SIZE)
            text = font.render(f'{node.ward}W', True, WARD_COLOR)
            text_rect = text.get_rect(center=(x_center, y_center+WARD_RADIUS + 6))
            s.blit(text, text_rect)

        # Add info on the script and vector installation for the current node
        if player_route and node == player_route.node_path[-1]:
            installable_vector_count = len(script.vector)
            if installable_vector_count:
                box_width = installable_vector_count*(INSTALL_VECTOR_BORDER+1)+VECTOR_WIDTH+3
                box_height = VECTOR_SIZE[1]+INSTALL_VECTOR_BORDER*2
                box_left = x_center-box_width//2
                box_top = y_center+INSTALL_VECTOR_OFFSET

                pygame.draw.rect(s, 'blue', pygame.Rect((box_left, box_top),(box_width, box_height)))
                for ndx, vector in enumerate(script.vector):
                    new_mouseovers = render_vector(s,
                        box_left+ndx*VECTOR_WIDTH+(ndx+1)*INSTALL_VECTOR_BORDER,
                        box_top+INSTALL_VECTOR_BORDER,
                        vector, pygame.Color('#51FC45'))
                    mouseovers += new_mouseovers
                    interactables[f'INSTALL_VECTOR{ndx}'] = pygame.Rect((box_left+ndx*VECTOR_WIDTH+(ndx+1)*INSTALL_VECTOR_BORDER, box_top+INSTALL_VECTOR_BORDER), VECTOR_SIZE)

                # Add help text above vector box
                action_text = 'Overwrite Vector?' if node.vector else 'Install Vector?'
                font = pygame.font.Font(get_font('BrassMono', 'regular'), 14)
                text = font.render(action_text, True, 'white')
                text_rect = text.get_rect(center=(x_center, box_top+VECTOR_SIZE[1]+20))
                s.blit(text, text_rect)

            # Draw info on the executing player script
            s.blit(script_img, (x_center+SCRIPT_X_OFFSET, y_center+SCRIPT_Y_OFFSET))

            font = pygame.font.Font(get_font('BrassMono', 'bold'), 24)
            power_text = draw_text_with_outline(str(script.power), font, 'white', 1, 'black')
            text_rect = power_text.get_rect(center=(x_center+SCRIPT_X_OFFSET+SCRIPT_POWER_SIZE[0]//2, y_center+SCRIPT_Y_OFFSET+SCRIPT_POWER_SIZE[1]//2))
            s.blit(power_text, text_rect)

        # Draw info on the executing enemy script
        if enemy_route and node == enemy_route.node_path[-1] and enemy_script:
            s.blit(script_img, (x_center+ENEMY_SCRIPT_X_OFFSET, y_center+ENEMY_SCRIPT_Y_OFFSET))

            font = pygame.font.Font(get_font('BrassMono', 'bold'), 24)
            power_text = draw_text_with_outline(str(enemy_script.power), font, 'white', 1, 'black')
            text_rect = power_text.get_rect(center=(x_center+ENEMY_SCRIPT_X_OFFSET+SCRIPT_POWER_SIZE[0]//2, y_center+ENEMY_SCRIPT_Y_OFFSET+SCRIPT_POWER_SIZE[1]//2))
            s.blit(power_text, text_rect)

        s.blit(s, (0, 0))

    return interactables, mouseovers


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