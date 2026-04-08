import pygame
from camera import camera
from player import Player

from input import is_key_pressed

sprites = []
loaded = {}


class Sprite:
    def __init__(self, image, x, y, width=None, height=None):
        if image in loaded:
            self.image = loaded[image]
        else:
            img = pygame.image.load(image).convert_alpha()
            if width and height:
                img = pygame.transform.scale(img, (width, height))
            loaded[image] = img
            self.image = img

        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Create the rectangle for collision
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        sprites.append(self)

    def update_rect(self):

        self.rect.topleft = (self.x, self.y)

    def collides_with(self, other):
        while True:
            return self.rect.colliderect(other.rect)

    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        self.update_rect()
        screen.blit(self.image, (self.x - camera.x, self.y - camera.y))
