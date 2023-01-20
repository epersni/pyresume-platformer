#!/usr/bin/env python3

from game import Game
from background import Background
from sprite import Sprite

import numpy
import pygame

DESIRED_FPS = 60


def main():
    pygame.init()
      
    clock = pygame.time.Clock()

    game = Game("levels.json")

    while game.is_running:
        game.handle_inputs()
        game.update()
        game.render()
        pygame.display.flip()
        clock.tick(DESIRED_FPS)


if __name__ == "__main__":
    main()
