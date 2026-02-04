import pygame


def draw_text_with_outline(text, font, color, outline_size, outline_color):
    text_render = font.render(text, True, outline_color)
    text_size = text_render.get_size()
    surface = pygame.Surface((text_size[0] + outline_size*2, text_size[1] + outline_size*2), pygame.SRCALPHA)
    surface_rect = surface.get_rect()
    offsets = [(ox, oy)
        for ox in range(-outline_size, outline_size+1)
        for oy in range(-outline_size, outline_size+1)]
    for ox, oy in offsets:
        px, py = surface_rect.center
        surface.blit(text_render, text_render.get_rect(center = (px+ox, py+oy)))
    inner_text = font.render(text, True, color).convert_alpha()
    surface.blit(inner_text, inner_text.get_rect(center=surface_rect.center))
    return surface
