#!/usr/bin/env python3

import json
import math
import numpy
import pygame


BACKGROUND_COLOR = (0, 0, 0)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Background:
    def __init__(self, width, height):
        self.tile_group = pygame.sprite.Group()
        self.image_path = "graphics/background.png"

        image = pygame.image.load(self.image_path)

        print(f"image_width={image.get_width()}")
        print(f"image_height={image.get_height()}")
        print(f"division={math.ceil((width+0.5)/image.get_width())}")
        for x in range(0, math.ceil((width + 0.5) / image.get_width())):
            for y in range(0, math.ceil((height + 0.5) / image.get_height())):
                print(f" Adding {x},{y}")
                self.tile_group.add(
                    Sprite(
                        self.image_path, x * image.get_width(), y * image.get_height()
                    )
                )

    def draw(self, screen):
        self.tile_group.draw(screen)


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("graphics/player_front.png", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("graphics/player_jump.png")
        self.walk_cycle = [
            pygame.image.load(f"graphics/player_walk{i:0>2}.png") for i in range(1, 12)
        ]
        self.animation_index = 0
        self.facing_left = False
        self.speed = 6
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 1
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()
        self.jump_sound = pygame.mixer.Sound("./sounds/jump.wav")
        self.onground = False

    def update(self, platforms):
        hsp = 0
        self.onground = platforms.on_platform(
            self, 0, 1
        )  # self.check_collision(0,1,platforms)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            hsp = self.speed
        else:
            self.image = self.stand_image

        if key[pygame.K_SPACE] and self.onground:
            self.jump_sound.play()
            self.vsp = -self.jumpspeed

        if self.prev_key[pygame.K_SPACE] and not key[pygame.K_SPACE]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = key

        if self.vsp < 10 and not self.onground:
            self.jump_animation()
            self.vsp += self.gravity
        
        self.pushed_by_platform(platforms)
        self.move(hsp, self.vsp, platforms)

    def walk_animation(self):
        if self.vsp != 0 and not self.onground:
            return

        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def pushed_by_platform(self, platforms):
        dy = 0
        while platforms.on_platform(self, 0, dy):
            dy += 1
        self.rect.move_ip([0, dy])

    def check_collision_with_wall(self, x):
        if self.rect.left + x <= 0:
            return True
        if self.rect.right + x >= pygame.display.Info().current_w:
            return True
        return False

    def move(self, x, y, platforms):
        dx = x
        dy = y

        while platforms.on_platform(self, 0, dy):
            dy -= numpy.sign(dy)

        while platforms.on_platform(self, dx, dy if self.jumpspeed > 0 else 0):
            dx -= numpy.sign(dx)

        while self.check_collision_with_wall(dx):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])


class Platforms:
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
        #self.frame_count += 1
        #if self.frame_count == self.level_config["frames_per_move"]:  # TODO shall be global
        #    self.frame_count = 0
        #    self.move_platforms_down(self.level_config["pixels_per_move"])

    def _move_platforms_down(self, pixels):
        for sprite in self.boxes.sprites():
            sprite.rect.move_ip([0, pixels])

    def draw(self, screen):
        self.boxes.draw(screen)


class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("graphics/boxAlt.png", startx, starty)

    @staticmethod
    def get_size():
        box = Box(0, 0)
        rect = box.image.get_rect()
        return [rect.width, rect.height]


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    music = pygame.mixer.Sound("./sounds/music.wav")
    music.play()

    display_info = pygame.display.Info()
    player = Player(display_info.current_w / 2, 500)

    platforms = Platforms(display_info.current_w, display_info.current_h)

    background = Background(800, 600)

    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)
        background.draw(screen)
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            running = False
        platforms.update()
        player.update(platforms)
        player.draw(screen)
        platforms.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
