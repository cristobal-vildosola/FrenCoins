import os

import pygame
from pygame.locals import *

from modulos.control.Player import Player
from modulos.control.Driver import Driver
from modulos.control.Joystick import XBoxJoystick
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
    player2 = Player(1, k_up=K_w, k_down=K_s, k_left=K_a, k_right=K_d)

    players = [player1, player2]

    # controles
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        print(joystick.get_name())
        if joystick.get_name().lower().rfind("xbox") != -1:
            joysticks.append(XBoxJoystick(joystick))

            if i < len(players):
                players[i].joystick = joysticks[i]

    driver = Driver(screen, players)
    while driver.running:
        driver.tick()

    return


if __name__ == "__main__":
    main()
