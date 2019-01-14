from pygame.locals import *

from modulos.control.Joystick import NullJoystick, Joystick
from modulos.utils import path
from modulos.elements.Character import Character

sprites = ['Anouk', 'Ardila', 'Checho', 'Diggo', 'FatCow', 'Lecaros', 'LittleFrank',
           'MrBear', 'Peibl', 'Pina', 'Shi', 'Tito', 'Tomimi']


class Player:
    def __init__(self, player_id: int, driver=None, joystick: Joystick = NullJoystick(),
                 k_up=K_UP, k_down=K_DOWN, k_left=K_LEFT, k_right=K_RIGHT):
        self.driver = driver
        self.id = player_id

        self.img = player_id % len(sprites)
        self.char: Character = None
        self.restart_char()

        self.joystick: Joystick = joystick

        # TODO settings keys by player id
        self.k_up = k_up
        self.k_down = k_down
        self.k_left = k_left
        self.k_right = k_right

    def set_driver(self, driver):
        self.driver = driver

    def actions(self, events, pressed):
        # eventos (solo player 1)
        if self.id == 0:
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == self.k_up:
                        self.driver.press_up(self)
                    if event.key == self.k_down:
                        self.driver.press_down(self)
                    if event.key == self.k_left:
                        self.driver.press_left(self)
                    if event.key == self.k_right:
                        self.driver.press_right(self)

                    if event.key == K_RETURN:
                        self.driver.press_main(self)
                    if event.key == K_ESCAPE:
                        self.driver.press_start(self)

            # teclas apretadas
            if pressed[self.k_up]:
                self.driver.hold_up(self)
            if pressed[self.k_down]:
                self.driver.hold_down(self)
            if pressed[self.k_left]:
                self.driver.hold_left(self)
            if pressed[self.k_right]:
                self.driver.hold_right(self)

        # joystick
        if self.joystick.hold_up():
            self.driver.hold_up(self)
        if self.joystick.hold_down():
            self.driver.hold_down(self)
        if self.joystick.hold_left():
            self.driver.hold_left(self)
        if self.joystick.hold_right():
            self.driver.hold_right(self)

        if self.joystick.press_up():
            self.driver.press_up(self)
        if self.joystick.press_down():
            self.driver.press_down(self)
        if self.joystick.press_left():
            self.driver.press_left(self)
        if self.joystick.press_right():
            self.driver.press_right(self)

        if self.joystick.press_main():
            self.driver.press_main(self)
        if self.joystick.press_start():
            self.driver.press_start(self)

        # actualizar valores anteriores del joystick
        self.joystick.update()
        return

    def img_path(self):
        return path(f'static/img/{sprites[self.img]}.png')

    def next_char(self):
        self.img = (self.img + 1) % len(sprites)
        self.char.change_image(self.img_path())
        return

    def prev_char(self):
        self.img = (self.img - 1) % len(sprites)
        self.char.change_image(self.img_path())
        return

    def restart_char(self):
        self.char = Character(self.id, self.img_path(),
                              x=50 + 50 * self.id, y=200)
        return
