import pygame
from upload_image import load_image


CARD_SIZE = 223, 312
K = 0.75
CARD_SIZE = CARD_SIZE[0] * K, CARD_SIZE[1] * K
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.field = [[] for i in range(7)]
        self.foundation = [[] for i in range(4)]
        self.foundation_rects = [
            pygame.rect.Rect(600, 50, *CARD_SIZE),
            pygame.rect.Rect(650 + CARD_SIZE[0], 50, *CARD_SIZE),
            pygame.rect.Rect(700 + 2 * CARD_SIZE[0], 50, *CARD_SIZE),
            pygame.rect.Rect(750 + 3 * CARD_SIZE[0], 50, *CARD_SIZE)
        ]
        self.moving_card = None

    def draw_card(self, card):
        self.screen.blit(card.get_image(), (card.rect.x, card.rect.y))

    def draw_background(self):
        image = load_image("other", "background.jpeg")
        pygame.draw.rect(image, (1, 50, 32), (50, 50, *CARD_SIZE), width=3, border_radius=int(K * 6))
        pygame.draw.rect(image, (1, 50, 32), self.foundation_rects[0], width=3, border_radius=int(K * 6))
        pygame.draw.rect(image, (1, 50, 32), self.foundation_rects[1], width=3, border_radius=int(K * 6))
        pygame.draw.rect(image, (1, 50, 32), self.foundation_rects[2], width=3, border_radius=int(K * 6))
        pygame.draw.rect(image, (1, 50, 32), self.foundation_rects[3], width=3, border_radius=int(K * 6))
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
        self.draw_decks(deck.deck, deck.drop_deck)
        self.draw_moving_card()

    def draw_moving_card(self):
        if self.moving_card is not None:
            self.draw_card(self.moving_card)

    def check_field(self):
        # print("\n".join(list(map(lambda x: "|" + "; ".join(list(map(lambda z: z.get_info(), x))), self.field))))
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
        for i in self.field:
            if card.rect.colliderect(i[-1].rect):
                i.append(card)
                if self.check_field():
                    return i[-2]
                else:
                    i.remove(i[-1])
                    break
        return False