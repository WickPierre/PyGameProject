import pygame
import random
from menu import main_menu
from upload_image import load_image


SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.set_mode().get_size()
CARD_SIZE = 223, 312
K = 0.65
CARD_SIZE = CARD_SIZE[0] * K, CARD_SIZE[1] * K
FPS = 60
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']


# Функция для создания колоды карт
def create_deck():
    return [Card(suit, rank, "close") for suit in SUITS for rank in RANKS]


# Функция для перемешивания колоды карт
def shuffle_deck(deck):
    random.shuffle(deck)


# Функция отрисовки игрового поля
def draw_background():
    image = load_image("other", "background.jpeg")
    pygame.draw.rect(image, (1, 50, 32), (50, 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    pygame.draw.rect(image, (1, 50, 32), (600, 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    pygame.draw.rect(image, (1, 50, 32), (650 + CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    pygame.draw.rect(image, (1, 50, 32), (700 + 2 * CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    pygame.draw.rect(image, (1, 50, 32), (750 + 3 * CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3)
    screen.blit(image, (0, 0))


class Card(pygame.sprite.Sprite):
    def __init__(self, suit, rank, status):
        super().__init__(all_sprites)
        self.suit = suit
        self.rank = rank
        self.card_face = load_image("cards", self.suit + "_" + self.rank + ".png")
        self.card_back = load_image("cards", "blue_back.png")
        self.status = status
        if self.status == "open":
            self.image = self.card_face
        else:
            self.image = self.card_back
        self.scale()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def scale(self):
        self.image = pygame.transform.scale(self.image, CARD_SIZE)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    deck = create_deck()
    shuffle_deck(deck)
    running = True
    main_menu()
    draw_background()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
                running = False
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()