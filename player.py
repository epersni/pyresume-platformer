from sprite import Sprite
import pygame
import numpy


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

    def update(self, world):
        hsp = 0
        self.onground = world.on_platform(self, 0, 1)  # self.check_collision(0,1,world)
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

        self.pushed_by_platform(world)
        self.move(hsp, self.vsp, world)

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

    def pushed_by_platform(self, world):
        dy = 0
        while world.on_platform(self, 0, dy):
            dy += 1
        self.rect.move_ip([0, dy])

    def check_collision_with_wall(self, x):
        if self.rect.left + x <= 0:
            return True
        if self.rect.right + x >= pygame.display.Info().current_w:
            return True
        return False

    def move(self, x, y, world):
        dx = x
        dy = y

        while world.on_platform(self, 0, dy):
            dy -= numpy.sign(dy)

        while world.on_platform(self, dx, dy if self.jumpspeed > 0 else 0):
            dx -= numpy.sign(dx)

        while self.check_collision_with_wall(dx):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])
