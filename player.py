from sprite import Sprite
import pygame
import numpy
from importlib.resources import files
import resources


class Player(Sprite):
    def __init__(self, startx = 300, starty = 500):
        super().__init__(files('resources')/'player_front.png', startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load(files('resources')/'player_jump.png')
        self.walk_cycle = [
            pygame.image.load(files('resources')/f"player_walk{i:0>2}.png") for i in range(1, 12)
        ]
        self.animation_index = 0
        self.facing_left = False
        self.speed = 6
        self.jumpspeed = 20
        self.vsp = 0
        self.hsp = 0
        self.gravity = 1
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()
        self.jump_sound = pygame.mixer.Sound(files('resources')/'jump.wav')
        self.onground = False

    def jump(self):
        if self.onground:
            self.jump_sound.play()
            self.vsp = -self.jumpspeed
            self.image = self.jump_image
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

    def move_left(self):
        self.facing_left = True
        self.hsp = -self.speed

    def move_right(self):
        self.facing_left = False
        self.hsp = self.speed

    def stand(self):
        self.hsp = 0
        if self.onground:
            self.image = self.stand_image

    def is_dead(self):
        return self.rect.bottom >= 600

    def update(self, level):
        self.onground = level.on_platform(self, 0, 1)

        if self.hsp != 0:
            self.walk_animation()
        else:
            self.stand()

        if self.vsp < 10 and not self.onground:
            self.vsp += self.gravity
            self.image = self.jump_image
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

        self.pushed_by_platform(level)
        self.move(self.hsp, self.vsp, level)
        self.onground = level.on_platform(self, 0, 1)  # self.check_collision(0,1,level)

    def walk_animation(self):
        if self.vsp < 0 and not self.onground:
            return

        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def pushed_by_platform(self, level):
        dy = 0
        while level.on_platform(self, 0, dy):
            dy += 1
        self.rect.move_ip([0, dy])

    def check_collision_with_wall(self, x):
        if self.rect.left + x <= 0:
            return True
        if self.rect.right + x >= pygame.display.Info().current_w:
            return True
        return False

    def move(self, x, y, level):
        dx = x
        dy = y

        while level.on_platform(self, 0, dy):
            dy -= numpy.sign(dy)

        while level.on_platform(self, dx, dy):
            dx -= numpy.sign(dx)

        while self.check_collision_with_wall(dx):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])
