# item.py
import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, image, message):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft=pos)
        self.message = message

    def picked_up(self):
        self.kill()
        return self.message
