from player import Player
from level import Level
from background import Background
from intro_screen import IntroScreen
from enum import Enum
import pygame
import json

SCREEN_WIDTH = 800  # TODO: config?
SCREEN_HEIGHT = 600  # TODO: config?
BACKGROUND_COLOR = (0, 0, 0)


class GameState(Enum):
    INTRO = 1
    PLAY_LEVEL = 2
    LEVEL_FINISHED = 3


class Game:
    def __init__(self, levels_config):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.music = pygame.mixer.Sound("./sounds/music.wav")
        self.music.play(loops=-1)
        self.background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.fill(BACKGROUND_COLOR)
        self.player = Player(300, 500)  # TODO from level design
        self.is_running = True
        self.level_is_moving = False
        self.state = GameState.INTRO
        with open("levels.json", "r") as levels_config:
            self.config = json.load(levels_config)
            print("loaded config")
        self.intro_screen = IntroScreen(self.config["intro"])
        self._set_level(0)

    def _set_level(self, stage_id):
        self.level_config = self.config["levels"][stage_id]
        self.level = Level(self.level_config, SCREEN_WIDTH, SCREEN_HEIGHT)

    def handle_inputs(self):
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            self.is_running = False

        if self.state is GameState.PLAY_LEVEL:
            if key[pygame.K_SPACE]:
                self.player.jump()
            elif key[pygame.K_LEFT]:
                self.player.move_left()
            elif key[pygame.K_RIGHT]:
                self.player.move_right()
            else:
                self.player.stand()
        elif self.state is GameState.INTRO:
            if key[pygame.K_RETURN]:
                self.state = GameState.PLAY_LEVEL

    def update(self):
        self.player.update(self.level)
        self.level.update(self.player)
        if (
            not self.level_is_moving and self.player.rect.top < SCREEN_HEIGHT / 2
        ):  # TODO: magic number
            self.level_is_moving = True
            self.level.set_fall_speed(1)

        if self.player.is_dead():
            self.is_running = False

        if self.level.completed:
            # self.is_running = False
            self.player = Player(300, 500)  # TODO from level design
            self.level_is_moving = False
            self._set_level(1)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.background.draw(self.screen)
        if self.state is GameState.PLAY_LEVEL:
            self.level.draw(self.screen)
            self.player.draw(self.screen)
        elif self.state is GameState.INTRO:
            self.intro_screen.draw(self.screen)
