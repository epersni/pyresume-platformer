from sprite import Sprite
import pygame

GREEN = (130, 190, 130)
WHITE = (255, 255, 255)
GRAY = (219, 219, 219)
RED = (211, 117, 117)

SCREEN_WIDTH = 800  # TODO: config?
SCREEN_HEIGHT = 600  # TODO: config?
ALIGNMENT = 30
TEXT_X = SCREEN_WIDTH / 4
TEXT_Y = 50
LEFT_COLUMN_X = TEXT_X - 150
LEFT_COLUMN_Y = TEXT_Y

ARROW_RIGHT_X = SCREEN_WIDTH - 60
ARROW_LEFT_X = 60
ARROW_Y = SCREEN_HEIGHT - 50


class ExperienceScreen:
    def __init__(self, levels_config, initial_experience_id=0):
        self.config = levels_config
        self.selected_id = initial_experience_id
        self.title_font = pygame.font.SysFont("freesansbold", 24)
        self.company_font = pygame.font.SysFont("freesansbold", 24)
        self.description_font = pygame.font.SysFont("freesansbold", 24)
        self.keyword_font = pygame.font.SysFont("freesansbold", 24)
        self.header_font = pygame.font.SysFont("freesansbold", 24)
        self.unlocked_title_font = pygame.font.SysFont("freesansbold", 36)
        self.unlocked_instruction_font = pygame.font.SysFont("freesansbold", 24)
        self.header_font.underline = True
        self.line_count = 0

    def show_next(self):
        self.selected_id += 1
        if self.selected_id >= len(self.config):
            self.selected_id = len(self.config)-1

    def show_prev(self):
        self.selected_id -= 1
        if self.selected_id < 0:
            self.selected_id = 0

    def unlock_selected(self):
        self.config[self.selected_id]["unlocked"] = True

    def draw(self, screen):
        self.line_count = 0
        experience = self.config[self.selected_id]
        if self.selected_id > 0:
            self._draw_left_arrow(screen)
        if self.selected_id < len(self.config)-1:
            self._draw_righ_arrow(screen)
        self._draw_period(screen)
        if "unlocked" in experience and experience["unlocked"]:
            self._draw_title(screen)
            self._draw_company(screen)
            self._draw_description(screen)
            self._draw_keywords(screen)
        else:
            self._draw_locked_experience(screen)

    def _draw_righ_arrow(self, screen):
        arrow = Sprite("graphics/arrow_right.png", ARROW_RIGHT_X, ARROW_Y)
        arrow.draw(screen)

    def _draw_left_arrow(self, screen):
        arrow = Sprite("graphics/arrow_left.png", ARROW_LEFT_X, ARROW_Y)
        arrow.draw(screen)

    def _draw_locked_experience(self, screen):
        title = self.unlocked_title_font.render("Locked Experience", True, RED)
        screen.blit(title, (TEXT_X, TEXT_Y))
        instruction = self.unlocked_instruction_font.render(
            "Hit ENTER to play and unlock this experience", True, WHITE
        )
        screen.blit(instruction, (TEXT_X, TEXT_Y + ALIGNMENT))

    def _draw_company(self, screen):
        company_text = self.config[self.selected_id]["company"]
        company = self.title_font.render(company_text, True, GREEN)
        self._draw_text_line(screen, company)

    def _draw_title(self, screen):
        title_text = self.config[self.selected_id]["title"]
        title = self.title_font.render(title_text, True, GREEN)
        self._draw_text_line(screen, title)

    def _draw_period(self, screen):
        period_text = self.config[self.selected_id]["time_period"]
        period = self.title_font.render(period_text, True, GRAY)
        screen.blit(period, (LEFT_COLUMN_X, LEFT_COLUMN_Y))

    def _draw_description(self, screen):
        self._draw_header(screen, "Description")
        description = self.config[self.selected_id]["description"]
        for row, line in enumerate(description):
            line_text = self.description_font.render(line, True, GRAY)
            self._draw_text_line(screen, line_text)

    def _draw_keywords(self, screen):
        keywords = ", ".join(self.config[self.selected_id]["keywords"])
        keywords_text = self.keyword_font.render(keywords, True, GRAY)
        self._draw_header(screen, "Skills")
        self._draw_text_line(screen, keywords_text)

    def _draw_header(self, screen, header_text):
        header_text = self.header_font.render(header_text, True, GRAY)
        self._draw_text_line(screen, header_text)

    def _draw_text_line(self, screen, line_text):
        screen.blit(line_text, (TEXT_X, TEXT_Y + (ALIGNMENT * self.line_count)))
        self.line_count += 1
