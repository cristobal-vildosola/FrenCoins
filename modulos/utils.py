import os
import sys

import pygame

from settings.GUI import SCREEN_WIDTH, SCREEN_HEIGHT


def path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def center_screen():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    return


def hide_moude():
    pygame.mouse.set_cursor((8, 8), (0, 0), [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    return


def init_screen():
    pygame.init()

    center_screen()
    hide_moude()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("FrenCoins")
    pygame.display.set_icon(pygame.image.load(path('static/img/favicon.png')))

    return screen
