#!/usr/bin/env python3

from world import World
from player import Player
from background import Background
from sprite import Sprite

import json
import numpy
import pygame


BACKGROUND_COLOR = (0, 0, 0)

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    music = pygame.mixer.Sound("./sounds/music.wav")
    music.play()

    display_info = pygame.display.Info()
    player = Player(display_info.current_w / 2, 500)

    world = World(display_info.current_w, display_info.current_h)

    background = Background(800, 600)

    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)
        background.draw(screen)
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            running = False
        world.update()
        player.update(world)
        player.draw(screen)
        world.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
