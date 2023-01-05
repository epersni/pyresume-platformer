import pygame

GREEN = (130, 190, 130)
BLACK = (0, 0, 0)


class KeywordText:
    def __init__(self, text, startx, starty):
        self.font = pygame.font.SysFont("freesansbold", 72)
        self.text = self.font.render(text, True, GREEN, BLACK)
        self.rect = self.text.get_rect()
        self.startx = startx
        self.starty = starty

    def draw(self, screen):
        screen.blit(self.text, (self.startx, self.starty))
        pygame.draw.rect(self.text, GREEN, self.rect, 1)

    def move(self, dx, dy):
        self.startx += dx
        self.starty += dy
