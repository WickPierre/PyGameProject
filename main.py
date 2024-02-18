import pygame
import random
from menu import main_menu
from upload_image import load_image


SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.set_mode().get_size()
CARD_SIZE = 223, 312
K = 0.75
CARD_SIZE = CARD_SIZE[0] * K, CARD_SIZE[1] * K
FPS = 60
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']


class Deck:
    def __init__(self):
        self.deck = create_deck()
        self.cards = self.deck.copy()
        self.shuffle()
        self.x, self.y, (self.w, self.h) = 50, 50, CARD_SIZE

    def shuffle(self):
        random.shuffle(self.deck)

    def check_pos(self, x, y):
        if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
            return True
        return False

    def draw_card(self):
        if self.cards:
            card = self.cards[0]
            self.cards = self.cards[1:]
        else:
            return None
        return card

    def spread_cards(self):
        pass


# Функция для создания колоды карт
def create_deck():
    return [Card(suit, rank, "close") for suit in SUITS for rank in RANKS]


def is_card_clamped(x, y):
    for card in deck.deck:
        if card.check_pos(x, y) and card.is_movable:
            return card
    return False


# Функция отрисовки игрового поля
def draw_background():
    image = load_image("other", "background.jpeg")
    pygame.draw.rect(image, (1, 50, 32), (50, 50, CARD_SIZE[0], CARD_SIZE[1]), width=3, border_radius=int(K*6))
    pygame.draw.rect(image, (1, 50, 32), (600, 50, CARD_SIZE[0], CARD_SIZE[1]), width=3, border_radius=int(K*6))
    pygame.draw.rect(image, (1, 50, 32), (650 + CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3, border_radius=int(K*6))
    pygame.draw.rect(image, (1, 50, 32), (700 + 2 * CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3, border_radius=int(K*6))
    pygame.draw.rect(image, (1, 50, 32), (750 + 3 * CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3, border_radius=int(K*6))
    screen.blit(image, (0, 0))


class Card(pygame.sprite.Sprite):
    def __init__(self, suit, rank, status):
        super().__init__(all_sprites)
        self.suit = suit
        self.rank = rank
        self.is_movable = True
        self.card_face = load_image("cards", self.suit + "_" + self.rank + ".png", -1)
        self.card_back = load_image("cards", "red_back2.png", -1)
        self.scale()
        self.status = status
        if self.status == "open":
            self.image = self.card_face
        else:
            self.image = self.card_back
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50

    #     self._changed = False
    #
    # def __setattr__(self, key, value):
    #     if key != '_changed':
    #         self._changed = True
    #     super(Card, self).__setattr__(key, value)
    #
    # def is_status_changed(self):
    #     return self._changed

    def change_status(self, status):
        if status == "open":
            self.status = "open"
            self.image = self.card_face
        elif status == "close":
            self.status = "close"
            self.image = self.card_back

    def scale(self):
        self.card_face = pygame.transform.scale(self.card_face, CARD_SIZE)
        self.card_back = pygame.transform.scale(self.card_back, CARD_SIZE)

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def check_pos(self, x, y):
        if self.rect.x <= x <= self.rect.x + self.rect.width and self.rect.y <= y <= self.rect.y + self.rect.height:
            return True
        return False


if __name__ == '__main__':
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    deck = Deck()
    running = True
    main_menu()
    # x = 0
    # y = 0
    # for card in deck.deck:
    #     card.move(CARD_SIZE[0] * x, CARD_SIZE[1] * y)
    #     x += 1
    #     if x == 13:
    #         x = 0
    #         y += 1
    pos = None
    is_mouse_clamped = False
    current_card = None
    while running:
        draw_background()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if deck.check_pos(*event.pos):
                    current_card = deck.draw_card()
                    is_mouse_clamped = True
                if current_card := is_card_clamped(*event.pos):
                    current_card.change_status("open")
                    is_mouse_clamped = True
            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_clamped = False
            if event.type == pygame.MOUSEMOTION and is_mouse_clamped:
                current_card.move(*event.rel)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()