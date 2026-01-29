import pygame
import math
from dataclasses import dataclass


class MouseCheck:
    def __init__(self):
        self.reset()

    def on_interactable_object(self, x, y):
        # TODO: Account for potentially matching two overlapping objects
        for name, rect in self.rect_register.items():
            if rect.collidepoint(x, y):
                return name

        for name, circle in self.circle_register:
            if math.sqrt((circle.point[0]-x)**2 + (circle.point[1]-y)**2) <= circle.radius:
                return name

        return ''

    def on_mouseover_object(self, x, y):
        for tooltip in self.mouseover_register:
            if tooltip.rect.collidepoint(x, y):
                return tooltip.text

        return None

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
    text: str