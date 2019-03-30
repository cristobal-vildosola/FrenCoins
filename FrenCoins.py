from src.control.Driver import Driver
from src.utils import init_screen

import pygame


def main():
    screen = init_screen()
    driver = Driver(screen)

    while driver.running:
        driver.tick()
    pygame.quit()
    return


if __name__ == "__main__":
    main()
