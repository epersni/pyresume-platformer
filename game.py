from player import Player
from level import Level
from background import Background
import pygame
import json

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)


class Game:
    def __init__(self, levels_config):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.music = pygame.mixer.Sound("./sounds/music.wav")
        self.music.play()
        self.background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.fill(BACKGROUND_COLOR)
        self.level = Level(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = Player(300, 500)  # TODO from level design
        self.is_running = True
        self.level_is_moving = False

    def handle_inputs(self):
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            self.is_running = False
        elif key[pygame.K_SPACE]:
            self.player.jump()
        elif key[pygame.K_LEFT]:
            self.player.move_left()
        elif key[pygame.K_RIGHT]:
            self.player.move_right()
        else:
            self.player.stand()

    def update(self):
        self.player.update(self.level)
        self.level.update()
        if (
            not self.level_is_moving and self.player.rect.top < SCREEN_HEIGHT / 2
        ):  # TODO: magic number
            self.level_is_moving = True
            self.level.set_fall_speed(1)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.background.draw(self.screen)
        self.level.draw(self.screen)
        self.player.draw(self.screen)
