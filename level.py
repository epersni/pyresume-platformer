from box import Box
from keyword_text import KeywordText
from sprite import Sprite
import pygame
import json


class Level:
    def __init__(self, config, level_width, level_height):
        self.frame_count = 0
        self.boxes = pygame.sprite.Group()
        self.available_keywords = []
        self.vsp = 0
        self.key = Sprite("graphics/key.png", 0, 0)
        self.collected_keywords = []
        self.collect_sound = pygame.mixer.Sound("./sounds/collect.wav")
        self.completed = False

        #with open("levels.json", "r") as levels_config:
        #    levels_config = json.load(levels_config)
        #    levels = levels_config["levels"]
        self.level_config = config
        boxes = self.level_config["boxes"]
        box_size = Box.get_size()[0]
        keyword_count = 0
        for row, line in enumerate(reversed(boxes)):
            for column, box in enumerate(line):
                if box == "*":
                    self.boxes.add(
                        Box(column * box_size, level_height - (row * box_size))
                    )
                elif box == "f":
                    self.key.rect.move_ip(
                        column * box_size, level_height - (row * box_size)
                    )

                elif box == "k":
                    keyword = self.level_config["keywords"][keyword_count]
                    keyword_count += 1
                    self.available_keywords.append(
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

    def set_fall_speed(self, vsp):
        self.vsp = vsp

    def update(self, player):
        self._move_platforms_down(self.vsp)
        self._move_keywords_down(self.vsp)
        self.key.rect.move_ip([0, self.vsp])
        for keyword in self.available_keywords:
            if player.rect.colliderect(keyword.rect):
                self.collect_sound.play()
                self.collected_keywords.append(keyword)
                self.available_keywords.remove(keyword)
        if player.rect.colliderect(self.key.rect):
            self.completed = True

    def _move_platforms_down(self, pixels):
        for sprite in self.boxes.sprites():
            sprite.rect.move_ip([0, pixels])

    def _move_keywords_down(self, pixels):
        for key in self.available_keywords:
            key.move(0, pixels)

    def draw(self, screen):
        self.boxes.draw(screen)
        for key in self.available_keywords:
            key.draw(screen)
        self.key.draw(screen)
