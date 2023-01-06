import pygame

GREEN = (130, 190, 130)
BLACK = (0, 0, 0)


class KeywordText:
    def __init__(self, text, startx, starty):
        self.font = pygame.font.SysFont("freesansbold", 36)
        self.text = self.font.render(text, True, GREEN, BLACK)
        self.rect = self.text.get_rect()
        pygame.draw.rect(self.text, GREEN, self.rect, 1)
        self.rect.move_ip([startx, starty])

    def draw(self, screen):
        screen.blit(self.text, self.rect)

    def move(self, dx, dy):
        self.rect.move_ip([dx, dy])
