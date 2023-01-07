from player import Player
from level import Level
from experience_screen import ExperienceScreen
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
    SHOW_EXPERIENCES = 3


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
        self.intro_screen = IntroScreen(self.config["intro"])
        self.experience_screen = ExperienceScreen(self.config["levels"])
        self.current_level_id = 0
        self.level = Level(
            self.config["levels"][self.current_level_id], SCREEN_WIDTH, SCREEN_HEIGHT
        )

    def handle_inputs(self):
        pygame.event.pump()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.is_running = False

            if self.state is GameState.PLAY_LEVEL:
                if keys[pygame.K_SPACE]:
                    self.player.jump()
                elif keys[pygame.K_LEFT]:
                    self.player.move_left()
                elif keys[pygame.K_RIGHT]:
                    self.player.move_right()
                else:
                    self.player.stand()
            elif self.state is GameState.INTRO:
                if keys[pygame.K_RETURN]:
                    self.state = GameState.PLAY_LEVEL
            elif self.state is GameState.SHOW_EXPERIENCES:
                if keys[pygame.K_RETURN]:
                    self.state = GameState.PLAY_LEVEL
                    next_level = self.experience_screen.selected_id
                    self.level = Level(
                        self.config["levels"][next_level], SCREEN_WIDTH, SCREEN_HEIGHT
                    )
                elif event.type == pygame.KEYDOWN and keys[pygame.K_LEFT]:
                    self.experience_screen.show_prev()
                elif event.type == pygame.KEYDOWN and keys[pygame.K_RIGHT]:
                    self.experience_screen.show_next()

    def update(self):
        if self.state is GameState.PLAY_LEVEL:
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
                self.state = GameState.SHOW_EXPERIENCES
                self.player = Player(300, 500)  # TODO from level design
                self.level_is_moving = False
                self.experience_screen.unlock_selected()

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.background.draw(self.screen)
        if self.state is GameState.PLAY_LEVEL:
            self.level.draw(self.screen)
            self.player.draw(self.screen)
        elif self.state is GameState.INTRO:
            self.intro_screen.draw(self.screen)
        elif self.state is GameState.SHOW_EXPERIENCES:
            self.experience_screen.draw(self.screen)
