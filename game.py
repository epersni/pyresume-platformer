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
        self.is_running = True

    def handle_inputs(self):
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            self.is_running = False

    def update(self):
        print(f"Updating...")

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.background.draw(self.screen)
        self.level.draw(self.screen)
        # level.update()
