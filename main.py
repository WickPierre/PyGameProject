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


def is_card_clamped(x, y):
    for card in deck.deck:
        if card.check_pos(x, y) and card.is_movable:
            return True
    return False


# Функция отрисовки игрового поля
def draw_background():
    image = load_image("other", "background.jpeg")
    pygame.draw.rect(image, (1, 50, 32), (50, 50, CARD_SIZE[0], CARD_SIZE[1]), width=3,
                     border_radius=int(K*6))
    pygame.draw.rect(image, (1, 50, 32), (600, 50, CARD_SIZE[0], CARD_SIZE[1]), width=3,
                     border_radius=int(K*6))
    pygame.draw.rect(image, (1, 50, 32), (650 + CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3,
                     border_radius=int(K*6))
    pygame.draw.rect(image, (1, 50, 32), (700 + 2 * CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3,
                     border_radius=int(K*6))
    pygame.draw.rect(image, (1, 50, 32), (750 + 3 * CARD_SIZE[0], 50, CARD_SIZE[0], CARD_SIZE[1]), width=3,
                     border_radius=int(K*6))
    screen.blit(image, (0, 0))


class Deck:
    def __init__(self):
        self.deck = []
        self.drop_deck = []
        self.field = []
        self.create_deck()
        self.cards = self.deck.copy()
        self.spread_cards()
        self.x, self.y, (self.w, self.h) = 50, 50, CARD_SIZE
        self.d_x, self.d_y = 250, 50

    def create_deck(self):
        self.deck = [(suit, rank, "close", "deck") for suit in SUITS for rank in RANKS]
        random.shuffle(self.deck)
        self.deck = list(map(lambda x: Card(*x), self.deck))
        # self.field = list(map(lambda x: x.set_mobility(False), self.deck[:29]))

    def shuffle(self):
        random.shuffle(self.deck)
        self.deck = map(lambda x: Card(*x), self.deck)

    def check_pos(self, x, y, kind):
        if kind == "deck":
            if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
                return True
        else:
            if self.d_x <= x <= self.d_x + self.w and self.d_y <= y <= self.d_y + self.h:
                return True
        return False

    def draw_card(self, start=False):
        if start:
            if self.cards:
                card = self.cards[0]
                self.cards = self.cards[1:]
                return card
        else:
            if self.drop_deck:
                card = self.drop_deck[-1]
                self.drop_deck = self.drop_deck[:-1]
                return card
        return Card("hearts", "ace", "open", "deck")  # will be fixed in the future

    def take_card(self):
        if self.cards:
            card = self.cards[0]
            card.move(200, 0)
            card.change_status("open")
            self.drop_deck.append(card)
            self.cards = self.cards[1:]
        else:
            self.cards = self.drop_deck
            self.drop_deck = []
            _ = [i.move(-200, 0) for i in self.cards]
            _ = [i.change_status("close") for i in self.cards]

    def spread_cards(self):
        y = 300
        for i in range(8):
            flag = True
            for j in range(i, 7):
                card = self.draw_card(True)
                if flag:
                    card.change_status("open")
                    flag = False
                card.move_to(300 + 200 * j, y)
            y += 50


class Card(pygame.sprite.Sprite):
    def __init__(self, suit, rank, status, kind):
        super().__init__(all_sprites)
        self.suit = suit
        self.rank = rank
        self.is_movable = True
        self.kind_of_card = kind
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

    def set_mobility(self, value):
        self.is_movable = value
        return self

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

    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y

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
    main_menu()
    # x = 0
    # y = 0
    # for card in deck.deck:
    #     card.move(CARD_SIZE[0] * x, CARD_SIZE[1] * y)
    #     x += 1
    #     if x == 13:
    #         x = 0
    #         y += 1
    running = True
    pos = None
    is_mouse_clamped = False
    is_card_taken = False
    current_card = None
    deck = Deck()
    while running:
        draw_background()
        # deck.spread_cards()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if deck.check_pos(*event.pos, "deck"):
                    is_card_taken = True
                elif deck.check_pos(*event.pos, "drop_deck"):
                    if is_card_clamped(*event.pos):
                        current_card = deck.draw_card()
                        is_mouse_clamped = True
            if event.type == pygame.MOUSEBUTTONUP:
                if is_card_taken:
                    deck.take_card()
                    is_card_taken = False
                is_mouse_clamped = False
            if event.type == pygame.MOUSEMOTION and is_mouse_clamped:
                current_card.move(*event.rel)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()