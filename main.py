import pygame
import random
from menu import main_menu
from upload_image import load_image
from game_manager import Game
from config import FPS, CARD_SIZE, K, SUITS, RANKS, SCREEN_WIDTH, SCREEN_HEIGHT


BUTTON_SIZE = SCREEN_WIDTH / 8, SCREEN_HEIGHT / 16


class MenuButton:
    def __init__(self, screen):
        self.screen = screen
        self.button_color = (0, 100, 20)
        self.font_small = pygame.font.SysFont(None, 65)
        self.x = 1650
        self.y = 25
        self.text = "Menu"
        self.button = pygame.draw.rect(self.screen, self.button_color,(self.x, self.y, *BUTTON_SIZE), border_radius=25)

    def draw(self):
        self.button = pygame.draw.rect(self.screen, self.button_color,(self.x, self.y, *BUTTON_SIZE), border_radius=25)
        text = self.font_small.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.button.center)
        self.screen.blit(text, text_rect)


class RestartGameButton(MenuButton):
    def __init__(self):
        super().__init__(screen)
        self.x = 1650
        self.y = 110
        self.text = "Restart"


class ShowStatsButton(MenuButton):
    def __init__(self):
        super().__init__(screen)
        self.x = 1650
        self.y = 195
        self.text = "Statistics"


def move_cards_to_card(cards, destination_card):
    for item in cards:
        item.move_to_card(destination_card)
        destination_card = item


def return_back_several_cards(x, y, cards):
    for item in cards:
        item.move_to(x, y)
        y += 40


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

    def move_to_card(self, destination_card):
        self.rect.x = destination_card.rect.x
        self.rect.y = destination_card.rect.y + 40

    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    # def get_info(self):
    #     if self.status == "open":
    #         return f"{self.suit}, {self.rank}"
    #     return "XX"

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

    def take_card(self):
        if self.deck:
            card = self.deck[0]
            card.move(200, 0)
            card.change_status("open")
            self.drop_deck.append(card)
            self.deck = self.deck[1:]
        else:
            self.deck = self.drop_deck
            self.drop_deck = []
            _ = [item.move(-200, 0) for item in self.deck]
            _ = [item.change_status("close") for item in self.deck]

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

    def restart(self):
        self.deck = []
        self.drop_deck = []
        self.create_deck()
        self.spread_cards()


if __name__ == '__main__':
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    response = main_menu()
    if response == "close game":
        pygame.quit()
    gm = Game(screen)  # game manager
    deck = Deck()
    menu_button = MenuButton(screen)
    restart_game_button = RestartGameButton()
    show_stats_button = ShowStatsButton()
    stats_is_shown = False
    running = True
    card_taken = False
    card_taken_from_drop_deck = False
    one_card_taken_from_field = False
    several_cards_taken_from_field = False
    current_card = None
    current_cards = None
    old_column = None
    new_column = None
    old_coords = None
    stack = None
    rect = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                stats_is_shown = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                gm.collect_all_cards(deck)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.button.collidepoint(event.pos):
                    response = main_menu()
                    if response == "close game":
                        gm.restart()
                        running = False
                elif restart_game_button.button.collidepoint(event.pos):
                    gm.restart()
                    deck.restart()
                elif show_stats_button.button.collidepoint(event.pos):
                    stats_is_shown = True
                else:
                    coords = event.pos

                    if deck.deck_rect.collidepoint(coords):  # if we want to flip through the deck
                        card_taken = True

                    elif deck.collide_point_for_drop_deck(*coords):  # if we want to replace card from the drop deck
                        card_taken_from_drop_deck = True
                        current_card = deck.draw_card()
                        gm.moving_cards = [current_card]
                    
                    elif response := gm.point_collide_field_card(*coords):  # if we want to replace field card
                        if type(response[0]) is list:
                            current_cards, old_column = response
                            if current_cards[0].is_movable:
                                several_cards_taken_from_field = True
                                gm.take_cards_from(old_column, len(current_cards))
                                gm.moving_cards = current_cards
                                old_coords = current_cards[0].rect.x, current_cards[0].rect.y
                        else:
                            current_card, old_column = response
                            if current_card.is_movable:
                                one_card_taken_from_field = True
                                gm.take_card_from(old_column)
                                gm.moving_cards = [current_card]
                                old_coords = current_card.rect.x, current_card.rect.y

            if event.type == pygame.MOUSEBUTTONUP:
                if card_taken_from_drop_deck:
                    if stack := gm.point_collide_foundation_card(*event.pos):
                        stack -= 1
                        if gm.check_foundation_cards(current_card, stack):
                            current_card.move_to(gm.foundation_rects[stack].x, gm.foundation_rects[stack].y)
                            gm.replace_card_to_foundation(current_card, stack, old_column)
                        else:
                            current_card.move_to(*old_coords)

                    elif response := gm.collide_field_rect(current_card):
                        rect, i = response
                        gm.field[i].append(current_card)
                        current_card.move_to(rect.x, rect.y)

                    elif not (new_card := gm.collide_field_card(current_card)):
                        deck.return_back_card_to_drop_deck(current_card)

                    else:
                        current_card.move_to_card(new_card)
                    gm.moving_cards = []
                    card_taken_from_drop_deck = False

                if card_taken and deck.deck_rect.collidepoint(event.pos):
                    card_taken = False
                    deck.take_card()

                if one_card_taken_from_field:
                    if response := gm.point_collide_field_card(*event.pos):
                        new_card, new_column = response
                        if gm.check_field_card(current_card, new_column):
                            current_card.move_to_card(new_card)
                            gm.replace_card(current_card, old_column, new_column)
                        else:
                            gm.return_back_card_to(current_card, old_column)
                            current_card.move_to(*old_coords)

                    elif response := gm.collide_field_rect(current_card):
                        rect, new_column = response
                        current_card.move_to(rect.x, rect.y)
                        gm.replace_card(current_card, old_column, new_column)

                    elif stack := gm.point_collide_foundation_card(*event.pos):
                        stack -= 1
                        if gm.check_foundation_cards(current_card, stack):
                            current_card.move_to(gm.foundation_rects[stack].x, gm.foundation_rects[stack].y)
                            gm.replace_card_to_foundation(current_card, stack, old_column)
                        else:
                            gm.return_back_card_to(current_card, old_column)
                            current_card.move_to(*old_coords)
                    else:
                        gm.return_back_card_to(current_card, old_column)
                        current_card.move_to(*old_coords)
                    gm.moving_cards = []
                    one_card_taken_from_field = False

                if several_cards_taken_from_field:
                    if response := gm.point_collide_field_card(*event.pos):
                        new_card, new_column = response
                        if gm.check_field_cards(current_cards, new_column):
                            move_cards_to_card(current_cards, new_card)
                            gm.replace_cards(current_cards, old_column, new_column)
                        else:
                            gm.return_back_cards_to(current_cards, old_column)
                            return_back_several_cards(*old_coords, current_cards)

                    elif response := gm.collide_field_rect(current_cards[0]):
                        rect, new_column = response
                        current_cards[0].move_to(rect.x, rect.y)
                        move_cards_to_card(current_cards[1:], current_cards[0])
                        gm.replace_cards(current_cards, old_column, new_column)

                    else:
                        gm.return_back_cards_to(current_cards, old_column)
                        return_back_several_cards(*old_coords, current_cards)
                    gm.moving_cards = []
                    several_cards_taken_from_field = False

            if event.type == pygame.MOUSEMOTION:
                if menu_button.button.collidepoint(*event.pos):
                    menu_button.button_color = (0, 150, 20)
                else:
                    menu_button.button_color = (0, 100, 20)

                if restart_game_button.button.collidepoint(*event.pos):
                    restart_game_button.button_color = (0, 150, 20)
                else:
                    restart_game_button.button_color = (0, 100, 20)

                if show_stats_button.button.collidepoint(*event.pos):
                    show_stats_button.button_color = (0, 150, 20)
                else:
                    show_stats_button.button_color = (0, 100, 20)

                if card_taken_from_drop_deck or one_card_taken_from_field:
                    current_card.move(*event.rel)
                elif several_cards_taken_from_field:
                    for card in current_cards:
                        card.move(*event.rel)
        gm.render(deck)
        menu_button.draw()
        restart_game_button.draw()
        show_stats_button.draw()
        if stats_is_shown:
            gm.show_stats()
        if gm.check_win():
            gm.show_game_over_screen()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()