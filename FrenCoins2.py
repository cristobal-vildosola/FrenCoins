import os

import pygame

from modulos.Characters import Player
from modulos.Driver import Driver
from modulos.Joystick import XBoxJoystick
from modulos.utils import path


def main():
    pygame.init()
    # centrar ventana
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("FrenCoins")
    pygame.display.set_icon(pygame.image.load(path('static/img/favicon.png')))

    # personajes
    player1 = Player(0)
    players = [player1]

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

    driver = Driver(players, screen)
    while driver.running:
        driver.tick()

    return


if __name__ == "__main__":
    main()
