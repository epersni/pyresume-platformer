from box import Box
import pygame
import json


class World:
    def __init__(self, level_width, level_start):
        self.frame_count = 0
        self.boxes = pygame.sprite.Group()
        self.vsp = 0

        with open("levels.json", "r") as levels_config:
            levels_config = json.load(levels_config)
            levels = levels_config["levels"]
            self.level_config = levels[0]
            boxes = self.level_config["boxes"]
            box_size = Box.get_size()[0]
            for row, line in enumerate(reversed(boxes)):
                for column, box in enumerate(line):
                    if box == "*":
                        self.boxes.add(
                            Box(column * box_size, level_start - (row * box_size))
                        )

    def on_platform(self, sprite, dx, dy):
        sprite.rect.move_ip([dx, dy])
        collide = pygame.sprite.spritecollideany(sprite, self.boxes)
        sprite.rect.move_ip([-dx, -dy])
        return collide

    def update(self):
        self._move_platforms_down(self.vsp)
        # self.frame_count += 1
        # if self.frame_count == self.level_config["frames_per_move"]:  # TODO shall be global
        #    self.frame_count = 0
        #    self.move_platforms_down(self.level_config["pixels_per_move"])

    def _move_platforms_down(self, pixels):
        for sprite in self.boxes.sprites():
            sprite.rect.move_ip([0, pixels])

    def draw(self, screen):
        self.boxes.draw(screen)
