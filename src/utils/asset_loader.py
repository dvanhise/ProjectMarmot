import os
import pygame
import __main__


# This shold work when running the raw project directly or from the bundled exe
BASE_DIR = os.path.dirname(__main__.__file__)
image_loader = None

class ImageLoader:
    IMAGES_DIR = os.path.join(BASE_DIR, 'assets', 'images')

    def __init__(self):
        self.registry = {}
        for filename in os.listdir(self.IMAGES_DIR):
            name, ext = filename.split('.')
            if ext in ['png', 'bmp', 'jpg', 'jpeg']:
                self.registry[name] = pygame.image.load(f'{self.IMAGES_DIR}/{filename}')
                # TODO: Resize here for efficiency?

    def get(self, name):
        return self.registry.get(name)


def img_fetch():
    global image_loader
    if not image_loader:
        image_loader = ImageLoader()
    return image_loader


def get_font(name: str, style: str):
    font_map = {
        'brassmono': {
            'regular': 'BrassMono-Regular.ttf',
            'bold': 'BrassMono-Bold.ttf'
        }
    }

    return os.path.join(BASE_DIR, 'assets', 'fonts', font_map[name.lower()][style.lower()])
