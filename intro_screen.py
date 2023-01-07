import pygame

GREEN = (130, 190, 130)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800  # TODO: config?
SCREEN_HEIGHT = 600  # TODO: config?
TEXT_ALIGNMENT = 50
TEXT_START_X = SCREEN_WIDTH / 2
TEXT_START_Y = SCREEN_HEIGHT / 2 - (TEXT_ALIGNMENT * 2)


class IntroScreen:
    def __init__(self, intro_config):
        self.text_lines = intro_config["body_text"]
        self.font = pygame.font.SysFont("freesansbold", 36)
        self.title = self.font.render(intro_config["title"], True, GREEN)
        self.title_rect = self.title.get_rect(center=(TEXT_START_X, TEXT_START_Y))

    def draw(self, screen):
        screen.blit(self.title, self.title_rect)
        for row, line in enumerate(self.text_lines):
            text = self.font.render(line, True, WHITE)
            text_center = text.get_rect(
                center=(TEXT_START_X, ((1 + row) * TEXT_ALIGNMENT) + (TEXT_START_Y))
            )
            screen.blit(text, text_center)
