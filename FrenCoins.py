import os

import pygame

from modulos.control.Driver import Driver
from modulos.utils import path


def main():
    pygame.init()

    # centrar ventana
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # mouse invisible
    pygame.mouse.set_cursor((8, 8), (0, 0), [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])

    screen_width, screen_height = 800, 600  # TODO: constant
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("FrenCoins")
    pygame.display.set_icon(pygame.image.load(path('static/img/favicon.png')))

    driver = Driver(screen)
    while driver.running:
        driver.tick()

    return


if __name__ == "__main__":
    main()
