from sprite import Sprite

import math
import pygame

class Background:
    def __init__(self, width, height):
        self.tile_group = pygame.sprite.Group()
        self.image_path = "graphics/background.png"

        image = pygame.image.load(self.image_path)

        for x in range(0, math.ceil((width + 0.5) / image.get_width())):
            for y in range(0, math.ceil((height + 0.5) / image.get_height())):
                self.tile_group.add(
                    Sprite(
                        self.image_path, x * image.get_width(), y * image.get_height()
                    )
                )

    def draw(self, screen):
        self.tile_group.draw(screen)

