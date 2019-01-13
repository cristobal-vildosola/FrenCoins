import os

import pygame
from pygame.locals import *

from modulos.control.Player import Player
from modulos.control.Driver import Driver
from modulos.control.Joystick import init_joystick
from modulos.utils import path


def main():
    pygame.init()
    # centrar ventana
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    screen_width, screen_height = 800, 600  # TODO: constant
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("FrenCoins")
    pygame.display.set_icon(pygame.image.load(path('static/img/favicon.png')))

    # personajes
    player1 = Player(0)

    # controles
    if pygame.joystick.get_count() > 0:
        joystick = init_joystick(0)
        player1.joystick = joystick

    driver = Driver(screen, [player1])
    while driver.running:
        driver.tick()

    return


if __name__ == "__main__":
    main()
