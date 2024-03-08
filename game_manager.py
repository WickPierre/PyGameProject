import pygame
from upload_image import load_image
from config import CARD_SIZE, K, SUITS, RANKS, SCREEN_WIDTH, SCREEN_HEIGHT


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.field = [[] for i in range(7)]
        self.field_rects = [
            pygame.rect.Rect(300, 300, *CARD_SIZE),
            pygame.rect.Rect(500, 300, *CARD_SIZE),
            pygame.rect.Rect(700, 300, *CARD_SIZE),
            pygame.rect.Rect(900, 300, *CARD_SIZE),
            pygame.rect.Rect(1100, 300, *CARD_SIZE),
            pygame.rect.Rect(1300, 300, *CARD_SIZE),
            pygame.rect.Rect(1500, 300, *CARD_SIZE),
        ]
        self.foundation = [[] for i in range(4)]
        self.foundation_rects = [
            pygame.rect.Rect(600, 50, *CARD_SIZE),
            pygame.rect.Rect(650 + CARD_SIZE[0], 50, *CARD_SIZE),
            pygame.rect.Rect(700 + 2 * CARD_SIZE[0], 50, *CARD_SIZE),
            pygame.rect.Rect(750 + 3 * CARD_SIZE[0], 50, *CARD_SIZE)
        ]
        self.wins = 0
        self.losses = 0
        self.load_stats()
        self.moving_cards = []

    def draw_card(self, card):
        self.screen.blit(card.get_image(), (card.rect.x, card.rect.y))

    def draw_background(self):
        image = load_image("other", "background.jpeg")
        pygame.draw.rect(image, (1, 50, 32), (50, 50, *CARD_SIZE), width=3, border_radius=int(K * 6))
        for i in self.foundation_rects:
            pygame.draw.rect(image, (1, 50, 32), i, width=3, border_radius=int(K * 6))
        for i in self.field_rects:
            pygame.draw.rect(image, (1, 50, 32), i, width=3, border_radius=int(K * 6))
        self.screen.blit(image, (0, 0))

    def draw_decks(self, deck, drop_deck):
        for card in deck:
            self.draw_card(card)
        for card in drop_deck:
            self.draw_card(card)

    def render(self, deck):
        self.draw_background()
        for cards in self.field:
            for card in cards:
                self.draw_card(card)
        for i in range(4):
            for card in self.foundation[i]:
                self.draw_card(card)
        self.draw_decks(deck.deck, deck.drop_deck)
        self.draw_moving_cards()

    def draw_moving_cards(self):
        if self.moving_cards:
            for card in self.moving_cards:
                self.draw_card(card)

    def check_field(self):
        for cards in self.field:
            e = []
            for card in cards:
                response = card.get_color_and_rank()
                if type(response) is tuple:
                    e.append(response)
            check_ranks = list(map(lambda x: x[1], e))
            check_colors = list(map(lambda x: x[0], e))
            if ", ".join(check_ranks[::-1]) not in ", ".join(RANKS):
                return False
            if "red, red" in ", ".join(check_colors) or "black, black" in ", ".join(check_colors):
                return False
        return True

    def collide_field_card(self, card):
        for i in range(len(self.field)):
            if self.field[i] and card.rect.colliderect(self.field[i][-1].rect):
                self.field[i].append(card)
                if self.check_field():
                    return self.field[i][-2]
                self.field[i].remove(self.field[i][-1])
                return False

    def collide_field_rect(self, card):
        for i in range(len(self.field)):
            if card.rect.colliderect(self.field_rects[i]) and card.rank == "king" and not self.field[i]:
                return self.field_rects[i], i

    def point_collide_field_card(self, x, y):
        for col in range(len(self.field)):
            for card in self.field[col][::-1]:
                if card.rect.collidepoint(x, y):
                    if card == self.field[col][-1]:
                        return card, col
                    else:
                        return self.field[col][self.field[col].index(card):], col
        return False

    def take_card_from(self, col):
        self.field[col] = self.field[col][:-1]

    def take_cards_from(self, col, index):
        self.field[col] = self.field[col][:-index]

    def return_back_card_to(self, card, col):
        self.field[col].append(card)

    def return_back_cards_to(self, cards, col):
        for card in cards:
            self.field[col].append(card)

    def point_collide_foundation_card(self, x, y):
        for i in range(4):
            if self.foundation_rects[i].collidepoint(x, y):
                return i + 1
        return False

    def replace_card(self, card, old_column, new_column):
        self.field[new_column].append(card)
        if self.field[old_column]:
            self.field[old_column][-1].change_status("open")

    def replace_cards(self, cards, old_column, new_column):
        for card in cards:
            self.field[new_column].append(card)
        if self.field[old_column]:
            self.field[old_column][-1].change_status("open")

    def replace_card_to_foundation(self, card, stack, old_column):
        if card in self.field[old_column]:
            self.field[old_column].remove(card)
        self.foundation[stack].append(card)
        if self.field[old_column]:
            self.field[old_column][-1].change_status("open")

    def check_field_card(self, card, column):
        self.field[column].append(card)
        answer = False
        if self.check_field():
            answer = True
        self.field[column].remove(card)
        return answer

    def check_field_cards(self, cards, column):
        for card in cards:
            self.field[column].append(card)
        answer = False
        if self.check_field():
            answer = True
        for card in cards:
            self.field[column].remove(card)
        return answer

    def check_foundation(self):
        for i in range(4):
            if self.foundation[i] and (", ".join(list(map(lambda x: x.rank, self.foundation[i]))) not in ", ".join(RANKS)
                                       or self.foundation[i][0].rank != "ace" or
                                       len(list(set(list(map(lambda x: x.suit, self.foundation[i]))))) != 1):
                return False
        return True

    def check_foundation_cards(self, card, stack):
        self.foundation[stack].append(card)
        answer = False
        if self.check_foundation():
            answer = True
        self.foundation[stack].remove(card)
        return answer

    def collect_all_cards(self, deck):
        is_card_collected = True
        while is_card_collected:
            is_card_collected = False
            for cards in self.field:
                card = cards[-1] if cards else False
                for stack in range(4):
                    if cards and cards[-1].is_movable and self.check_foundation_cards(card, stack):
                        self.replace_card_to_foundation(card, stack, self.field.index(cards))
                        card.move_to(self.foundation_rects[stack].x, self.foundation_rects[stack].y)
                        is_card_collected = True
                        break
            if deck.drop_deck:
                card = deck.drop_deck[-1]
                for stack in range(4):
                    if card.is_movable and self.check_foundation_cards(card, stack):
                        deck.draw_card()
                        self.foundation[stack].append(card)
                        card.move_to(self.foundation_rects[stack].x, self.foundation_rects[stack].y)
                        is_card_collected = True
                        break

    def restart(self):
        if self.check_win():
            self.wins += 1
        else:
            self.losses += 1
        self.change_stats()
        self.field = [[] for i in range(7)]
        self.foundation = [[] for i in range(4)]
        self.moving_cards = []

    def load_stats(self):
        with open("data/statistics/statistics.txt", "r") as file:
            self.wins, self.losses = map(int, ":".join(file.read().split("\n")).split(":")[1::2])

    def change_stats(self):
        with open("data/statistics/statistics.txt", "w") as file:
            file.write("Wins:" + str(self.wins) + "\n")
            file.write("Losses:" + str(self.losses))

    def check_win(self):
        if sum(list(map(lambda x: len(x), self.foundation))) == 52:
            return True
        return False

    def show_stats(self):
        font = pygame.font.Font(None, 250)
        image = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.SRCALPHA, 32)
        image.convert_alpha()
        pygame.draw.rect(image, (0, 0, 0, 100), (0, 0, 1920, 1080))
        pygame.draw.rect(image, (0, 100, 20), (400, 100, 1120, 880))
        wins_text = font.render(f"Wins: {self.wins}", True, (0, 0, 0))
        losses_text = font.render(f"Losses: {self.losses}", True, (0, 0, 0))
        image.blit(wins_text, (500, 200))
        image.blit(losses_text, (500, 600))
        self.screen.blit(image, (0, 0))

    def show_game_over_screen(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 150)
        text = font.render("You Won!!!", True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = self.screen.get_rect().center
        self.screen.blit(text, textRect)