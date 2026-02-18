import pygame
from src.render.network import NETWORK_HEIGHT
from src.constants import SCREEN_WIDTH, TERMINAL_GREEN, DARK_TERMINAL, CRT_TAN
from src.utils.asset_loader import get_font

TERM_SIZE = (250, 120)
TERM_FONT_SIZE = 11
TERM_PADDING = 8
TERM_LINE_SPACING = 12
MAX_LINE_CHARS = 38

PLAYER_TERM_OFFSET = (10, NETWORK_HEIGHT-TERM_SIZE[1])
ENEMY_TERM_OFFSET = (SCREEN_WIDTH-260, NETWORK_HEIGHT-TERM_SIZE[1])


def render_terminal(s: pygame.Surface, char):
    term_surface = pygame.Surface(TERM_SIZE)
    term_surface.fill(DARK_TERMINAL)
    pygame.draw.rect(term_surface, CRT_TAN, term_surface.get_rect(), width=5)

    font = pygame.font.Font(get_font('BrassMono', 'regular'), TERM_FONT_SIZE)

    lines = []

    if char.owner == 'ENEMY':
        offset = ENEMY_TERM_OFFSET
        if char.script:
            lines.append(f'>> init script --power={char.script.power}')
            for vector in char.script.vector:
                t = f'>> set vector {vector.name}'
                if vector.default_ward:
                    t += f' ward={vector.default_ward}'
                if vector.tags:
                    t += f' tags={",".join([t.get_full_name() for t in vector.tags])}'
                lines.append(t)

            if char.script.tags:
                lines.append(f'>> set {" ".join([t.get_full_name() for t in char.script.tags])}')

            # TODO: Add self-tags as well

    elif char.owner == 'PLAYER':
        offset = PLAYER_TERM_OFFSET
        if char.script:
            lines.append(f'>> init script --power={char.script.power}')
            for vector in char.script.vector:
                t = f'>> set vector {vector.name}'
                if vector.tags:
                    t += f' tags={",".join([t.get_full_name() for t in vector.tags])}'
                lines.append(t)

            if char.script.tags:
                lines.append(f'>> set {" ".join([t.get_full_name() for t in char.script.tags])}')

        else:
            # TODO: show action log when not executing a script
            pass

    else:
        raise ValueError(f'Unknown entity "{char.owner}"')

    # Apply text wrap for lone lines
    fixed_lines = []
    for line in lines:
        if len(line) > MAX_LINE_CHARS:
            fixed_lines.append(line[:MAX_LINE_CHARS])
            fixed_lines.append('    ' + line[MAX_LINE_CHARS:])
        else:
            fixed_lines.append(line)

    for ndx, line in enumerate(fixed_lines):
        text = font.render(line, True, TERMINAL_GREEN)
        text_rect = text.get_rect(topleft=(TERM_PADDING, TERM_PADDING+TERM_LINE_SPACING*ndx))
        term_surface.blit(text, text_rect)

    s.blit(term_surface, offset)

