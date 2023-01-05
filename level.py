from box import Box
from keyword_text import KeywordText
import pygame
import json


class Level:
    def __init__(self, level_width, level_height):
        self.frame_count = 0
        self.boxes = pygame.sprite.Group()
        self.keywords = []
        self.vsp = 0

        with open("levels.json", "r") as levels_config:
            levels_config = json.load(levels_config)
            levels = levels_config["levels"]
            self.level_config = levels[0]
            boxes = self.level_config["boxes"]
            box_size = Box.get_size()[0]
            keyword_count = 0
            for row, line in enumerate(reversed(boxes)):
                for column, box in enumerate(line):
                    if box == "*":
                        self.boxes.add(
                            Box(column * box_size, level_height - (row * box_size))
                        )
                    elif box == "k":
                        keyword = self.level_config["keywords"][keyword_count]
                        keyword_count += 1
                        self.keywords.append(
                            KeywordText(
                                keyword,
                                column * box_size,
                                level_height - (row * box_size),
                            )
                        )

    def on_platform(self, sprite, dx, dy):
        sprite.rect.move_ip([dx, dy])
        collide = pygame.sprite.spritecollideany(sprite, self.boxes)
        sprite.rect.move_ip([-dx, -dy])
        return collide

    def keyword_collide(self, sprite):
        collided_keywords = []
        for keyword in self.keywords:
            if sprite.rect.colliderect(keyword.rect):
                collided_keywords.append(keyword)
                self.keywords.remove(keyword)
        return collided_keywords

    def set_fall_speed(self, vsp):
        self.vsp = vsp

    def update(self):
        self._move_platforms_down(self.vsp)
        self._move_keywords_down(self.vsp)

    def _move_platforms_down(self, pixels):
        for sprite in self.boxes.sprites():
            sprite.rect.move_ip([0, pixels])

    def _move_keywords_down(self, pixels):
        for key in self.keywords:
            key.move(0, pixels)

    def draw(self, screen):
        self.boxes.draw(screen)
        for key in self.keywords:
            key.draw(screen)
