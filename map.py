import pygame
from camera import camera

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image)
        self.is_solid = is_solid


class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        self.tile_kinds = tile_kinds
        self.tile_size = tile_size
        self.tiles = []
        self.hitboxes = []

        with open(map_file, "r") as file:
            for y, line in enumerate(file.read().splitlines()):
                row = []
                for x, tile_char in enumerate(line):
                    tile_number = int(tile_char)
                    row.append(tile_number)

                    if self.tile_kinds[tile_number].is_solid:
                        hitbox = pygame.Rect(
                            x * tile_size,  # Use grid X position
                            y * tile_size,  # Use grid Y position
                            tile_size,  # Width
                            tile_size  # Height
                        )
                        self.hitboxes.append(hitbox)
                self.tiles.append(row)  # Add row AFTER processing line

        #Set world's "blocks"
        self.tile_size = tile_size
    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = (x * self.tile_size - camera.x, y * self.tile_size - camera.y)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)