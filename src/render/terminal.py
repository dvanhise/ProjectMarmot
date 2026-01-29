import pygame
from render.network import NETWORK_HEIGHT
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TERMINAL_GREEN, DARK_TERMINAL, CRT_TAN

TERM_SIZE = (250, 120)
TERM_FONT_SIZE = 11
TERM_PADDING = 8
TERM_LINE_SPACING = 12

PLAYER_TERM_OFFSET = (10, NETWORK_HEIGHT-TERM_SIZE[1])
ENEMY_TERM_OFFSET = (SCREEN_WIDTH-260, NETWORK_HEIGHT-TERM_SIZE[1])


def render_terminal(s: pygame.Surface, char):
    term_surface = pygame.Surface(TERM_SIZE)
    term_surface.fill(DARK_TERMINAL)
    pygame.draw.rect(term_surface, CRT_TAN, term_surface.get_rect(), width=5)

    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', TERM_FONT_SIZE)

    if char.owner == 'ENEMY' and char.script:
        vert_offset = TERM_PADDING
        text = font.render(f'>> init script --power={char.script.power}', True, TERMINAL_GREEN)
        text_rect = text.get_rect(topleft=(TERM_PADDING, vert_offset))
        term_surface.blit(text, text_rect)
        vert_offset += TERM_LINE_SPACING

        for vector in char.script.vector:
            t = f'>> set vector {vector.name}'
            if vector.tags:
                t += f' tags={",".join([t.get_full_name() for t in vector.tags])}'
            text = font.render(t, True, TERMINAL_GREEN)
            text_rect = text.get_rect(topleft=(TERM_PADDING, vert_offset))
            term_surface.blit(text, text_rect)
            vert_offset += TERM_LINE_SPACING

        if char.script.tags:
            text = font.render(f'>> set {" ".join([t.get_full_name() for t in char.script.tags])}', True, TERMINAL_GREEN)
            text_rect = text.get_rect(topleft=(TERM_PADDING, vert_offset))
            term_surface.blit(text, text_rect)

        s.blit(term_surface, ENEMY_TERM_OFFSET)
    elif char.owner == 'PLAYER':
        if char.script:
            vert_offset = TERM_PADDING
            text = font.render(f'>> init script --power={char.script.power}', True, TERMINAL_GREEN)
            text_rect = text.get_rect(topleft=(TERM_PADDING, vert_offset))
            term_surface.blit(text, text_rect)
            vert_offset += TERM_LINE_SPACING

            for vector in char.script.vector:
                t = f'>> set vector {vector.name}'
                if vector.tags:
                    t += f' tags={",".join([t.get_full_name() for t in vector.tags])}'
                text = font.render(t, True, TERMINAL_GREEN)
                text_rect = text.get_rect(topleft=(TERM_PADDING, vert_offset))
                term_surface.blit(text, text_rect)
                vert_offset += TERM_LINE_SPACING

            if char.script.tags:
                text = font.render(f'>> set {" ".join([t.get_full_name() for t in char.script.tags])}', True,
                                   TERMINAL_GREEN)
                text_rect = text.get_rect(topleft=(TERM_PADDING, vert_offset))
                term_surface.blit(text, text_rect)
        else:
            # TODO: show action log when not executing a script
            pass
        s.blit(term_surface, PLAYER_TERM_OFFSET)

