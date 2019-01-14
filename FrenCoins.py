from modulos.control.Driver import Driver
from modulos.utils import init_screen


def main():
    screen = init_screen()
    driver = Driver(screen)

    while driver.running:
        driver.tick()
    return


if __name__ == "__main__":
    main()
