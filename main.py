import pygame
import random
import menu
from upload_image import load_image


SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.set_mode().get_size()
CARD_SIZE = 223, 312
K = 0.65
CARD_SIZE = CARD_SIZE[0] * K, CARD_SIZE[1] * K
FPS = 60
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']


# Функция отрисовки игрового поля
def draw_background():
    image = load_image("other", "background.jpeg")
    pygame.draw.rect(image, (1, 50, 32), (50, 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    pygame.draw.rect(image, (1, 50, 32), (600, 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    pygame.draw.rect(image, (1, 50, 32), (650 + CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    pygame.draw.rect(image, (1, 50, 32), (700 + 2 * CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    pygame.draw.rect(image, (1, 50, 32), (750 + 3 * CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    screen.blit(image, (0, 0))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True
    menu.main_menu()
    draw_background()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
                running = False
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()