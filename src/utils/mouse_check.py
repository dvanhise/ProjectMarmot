import pygame
import math
from dataclasses import dataclass


class MouseCheck:
    def __init__(self):
        self.reset()
        self.mouse_down_on = []

    def mouse_down(self, x, y):
        self.mouse_down_on = self.on_interactable_objects(x, y)

    def mouse_up(self):
        self.mouse_down_on = []

    def has_selected(self, x, y, name, has_mouse_down=True):
        for obj in self.on_interactable_objects(x, y):
            if obj == name and (name in self.mouse_down_on if has_mouse_down else True):
                return True
        return False

    def has_selected_prefix(self, x, y, prefix, has_mouse_down=True):
        for obj in self.on_interactable_objects(x, y):
            if obj.startswith(prefix) and (obj in self.mouse_down_on if has_mouse_down else True):
                return int(obj.replace(prefix, ''))
        return None

    def on_interactable_objects(self, x, y):
        matches = []
        for name, rect in self.rect_register.items():
            if rect.collidepoint(x, y):
                matches.append(name)

        for name, circle in self.circle_register:
            if math.sqrt((circle.point[0]-x)**2 + (circle.point[1]-y)**2) <= circle.radius:
                matches.append(name)

        return matches

    def on_mouseover_object(self, x, y):
        for tooltip in self.mouseover_register:
            if tooltip.rect.collidepoint(x, y):
                return tooltip.text

        return []

    def register_rect(self, rects: dict[str, pygame.Rect]):
        self.rect_register.update(rects)

    def register_circle(self, name, point, radius):
        self.circle_register[name] = Circle(point=point, radius=radius)

    def register_mouseover_rect(self, tooltips):
        self.mouseover_register += tooltips

    def reset(self):
        self.circle_register = {}
        self.rect_register = {}
        self.mouseover_register = []


@dataclass
class Circle:
    point: tuple[int]
    radius: int

@dataclass
class Tooltip:
    rect: pygame.Rect
    text: list[str]