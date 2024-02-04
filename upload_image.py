import pygame
import os
import sys


def load_image(sort, name):
    fullname = os.path.join('data/' + sort, name)
    print(fullname)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image