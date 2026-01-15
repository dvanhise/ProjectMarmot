import os
import pygame


image_loader = None

class ImageLoader:
    IMAGES_DIR = './assets/images'

    def __init__(self):
        self.registry = {}
        for filename in os.listdir(self.IMAGES_DIR):
            name, ext = filename.split('.')
            if ext in ['png', 'bmp', 'jpg', 'jpeg']:
                self.registry[name] = pygame.image.load(f'{self.IMAGES_DIR}/{filename}')
                # TODO: Resize here

    def get(self, name):
        return self.registry.get(name)


def img_fetch():
    global image_loader
    if not image_loader:
        image_loader = ImageLoader()
    return image_loader