import pygame
import random
from menu import main_menu
from upload_image import load_image
from game_manager import Game


CARD_SIZE = 223, 312
K = 0.75
CARD_SIZE = CARD_SIZE[0] * K, CARD_SIZE[1] * K
FPS = 60
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']


class Card:
    def __init__(self, suit, rank, status, kind):
        # super().__init__(all_sprites)
        self.suit = suit
        self.rank = rank
        self.color = "red" if self.suit in ['hearts', 'diamonds'] else "black"
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
        self.rect = pygame.rect.Rect(50, 50, *CARD_SIZE)

    def get_image(self):
        return self.image

    def change_status(self, status):
        if status == "open":
            self.status = "open"
            self.image = self.card_face
            self.is_movable = True
        elif status == "close":
            self.status = "close"
            self.image = self.card_back
            self.is_movable = False

    def scale(self):
        self.card_face = pygame.transform.scale(self.card_face, CARD_SIZE)
        self.card_back = pygame.transform.scale(self.card_back, CARD_SIZE)

    def move_to_deck(self):
        self.rect.x = deck.drop_deck_rect.x
        self.rect.y = deck.drop_deck_rect.y

    def move_to_card(self, card):
        self.rect.x = card.rect.x
        self.rect.y = card.rect.y + 40

    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def get_info(self):
        if self.status == "open":
            return f"{self.suit}, {self.rank}"
        return "XX"

    def get_color_and_rank(self):
        if self.status == "open":
            return self.color, self.rank
        else:
            return "XX"


class Deck:
    def __init__(self):
        self.deck = []
        self.drop_deck = []
        self.create_deck()

        self.spread_cards()
        self.deck_rect = pygame.rect.Rect(50, 50, *CARD_SIZE)
        self.drop_deck_rect = pygame.rect.Rect(250, 50, *CARD_SIZE)

    def collide_point_for_drop_deck(self, x, y):
        if self.drop_deck_rect.collidepoint(x, y) and self.drop_deck:
            return True
        return False

    def create_deck(self):
        self.deck = [Card(suit, rank, "close", "deck") for suit in SUITS for rank in RANKS]
        random.shuffle(self.deck)

    def draw_card(self, start=False):
        if start:
            if self.deck:
                card = self.deck[0]
                self.deck = self.deck[1:]
                return card
        else:
            if self.drop_deck:
                card = self.drop_deck[-1]
                self.drop_deck = self.drop_deck[:-1]
                return card
        return Card("hearts", "ace", "open", "deck")  # will be fixed in the future

    def take_card(self):
        if self.deck:
            card = self.deck[0]
            card.move(200, 0)
            card.change_status("open")
            self.drop_deck.append(card)
            self.deck = self.deck[1:]
            gm.draw_card(card)
        else:
            self.deck = self.drop_deck
            self.drop_deck = []
            _ = [i.move(-200, 0) for i in self.deck]
            _ = [i.change_status("close") for i in self.deck]

    def spread_cards(self):
        y = 300
        for i in range(8):
            flag = True
            for j in range(i, 7):
                card = self.draw_card(True)
                card.kind_of_card = "field"
                card.is_movable = flag
                if flag:
                    card.change_status("open")
                    flag = False
                card.move_to(300 + 200 * j, y)
                gm.field[j].append(card)
            y += 40

    def return_back_card_to_drop_deck(self, card):
        self.drop_deck.append(card)
        card.move_to_deck()


if __name__ == '__main__':
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    main_menu()
    gm = Game(screen)  # game manager
    running = True
    deck = Deck()
    card_taken = False
    card_taken_from_drop_deck = False
    card_taken_from_field = False
    current_card = None
    old_column = None
    new_column = None
    old_coords = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = event.pos

                if deck.deck_rect.collidepoint(coords):  # if we want to flip through the deck
                    card_taken = True

                elif deck.collide_point_for_drop_deck(*coords):  # if we want to replace card from the drop deck
                    card_taken_from_drop_deck = True
                    current_card = deck.draw_card()
                    gm.moving_card = current_card

                elif current_card := gm.point_collide_field_card(*coords, current_card):  # if we want to replace field card
                    current_card, old_column = current_card
                    if current_card.is_movable:
                        card_taken_from_field = True
                        gm.moving_card = current_card
                        old_coords = current_card.rect.x, current_card.rect.y

            if event.type == pygame.MOUSEBUTTONUP:
                if card_taken_from_drop_deck:
                    if not (new_card := gm.collide_field_card(current_card)):
                        deck.return_back_card_to_drop_deck(current_card)
                    else:
                        current_card.move_to_card(new_card)
                    gm.moving_card = None
                    card_taken_from_drop_deck = False

                if card_taken and deck.deck_rect.collidepoint(event.pos):
                    card_taken = False
                    deck.take_card()

                if card_taken_from_field:
                    if new_card := gm.point_collide_field_card(*event.pos, current_card):
                        new_card, new_column = new_card
                        if gm.check_field_card(current_card, new_column):
                            current_card.move_to_card(new_card)
                            gm.replace_card(current_card, old_column, new_column)
                        else:
                            current_card.move_to(*old_coords)
                    else:
                        current_card.move_to(*old_coords)
                    gm.moving_card = None
                    card_taken_from_field = False

            if event.type == pygame.MOUSEMOTION:
                if card_taken_from_drop_deck or card_taken_from_field:
                    current_card.move(*event.rel)
        gm.render(deck)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()