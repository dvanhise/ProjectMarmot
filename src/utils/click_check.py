import pygame
import math
from dataclasses import dataclass


class ClickCheck:
    def __init__(self):
        self.reset()

    def on_object(self, x, y):
        # TODO: Account for potentially matching two overlapping objects
        for name, rect in self.rect_register.items():
            if rect.collidepoint(x, y):
                return name

        for name, circle in self.circle_register:
            if math.sqrt((circle.point[0]-x)**2 + (circle.point[1]-y)**2) <= circle.radius:
                return name

        return ''

    def register_rect(self, rects: dict):
        self.rect_register.update(rects)

    def register_circle(self, name, point, radius):
        self.circle_register[name] = Circle(point=point, radius=radius)

    def reset(self):
        self.circle_register = {}
        self.rect_register = {}


@dataclass()
class Circle:
    point: tuple[int]
    radius: int