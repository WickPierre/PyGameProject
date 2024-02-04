import pygame
import os
import sys

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
GREEN = (0, 100, 20)
LIGHT_GREEN = (0, 150, 20)
FPS = 60


class Menu:
    def __init__(self, screen):
        self.screen = screen

        self.background = load_image("background.jpeg")

        self.font_large = pygame.font.SysFont(None, 144)
        self.font_small = pygame.font.SysFont(None, 72)
        self.start_button_color = GREEN
        self.exit_button_color = GREEN

        self.x_b = (SCREEN_WIDTH - (SCREEN_WIDTH / 4)) / 2
        self.h_b = SCREEN_HEIGHT / 2.4
        self.button_size = (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 12)
        self.start_button = pygame.draw.rect(self.screen, self.start_button_color, (self.x_b, self.h_b, *self.button_size),
                                             border_radius=25)
        self.exit_button = pygame.draw.rect(self.screen, self.exit_button_color, (self.x_b, self.h_b + 180, *self.button_size),
                                            border_radius=25)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        text_title = self.font_large.render("Пасьянс", True, (255, 255, 255))
        self.screen.blit(text_title, ((SCREEN_WIDTH - text_title.get_width()) / 2, 180))

        self.start_button = pygame.draw.rect(self.screen, self.start_button_color, (self.x_b, self.h_b, *self.button_size),
                                             border_radius=25)
        self.exit_button = pygame.draw.rect(self.screen, self.exit_button_color, (self.x_b, self.h_b + 180, *self.button_size),
                                            border_radius=25)

        text_start = self.font_small.render("Начать игру", True, (255, 255, 255))
        text_start_rect = text_start.get_rect(center=self.start_button.center)
        self.screen.blit(text_start, text_start_rect)

        text_exit = self.font_small.render("Выход", True, (255, 255, 255))
        text_exit_rect = text_exit.get_rect(center=self.exit_button.center)
        self.screen.blit(text_exit, text_exit_rect)


def main_menu():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Пасьянс")
    menu = Menu(screen)
    clock = pygame.time.Clock()
    while True:
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                if menu.start_button.collidepoint(mouse_x, mouse_y):
                    menu.start_button_color = LIGHT_GREEN
                else:
                    menu.start_button_color = GREEN
                if menu.exit_button.collidepoint(mouse_x, mouse_y):
                    menu.exit_button_color = LIGHT_GREEN
                else:
                    menu.exit_button_color = GREEN
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu.start_button.collidepoint(x, y):
                    return True
                elif menu.exit_button.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        clock.tick(FPS)