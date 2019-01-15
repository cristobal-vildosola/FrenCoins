from src.control.Joystick import NullJoystick, Joystick
from src.control.Keyboard import NullKeyboard, Keyboard
from src.elements.Character import Character
from src.utils import path

sprites = ['Anouk', 'Ardila', 'Checho', 'Diggo', 'FatCow', 'Lecaros', 'LittleFrank',
           'MrBear', 'Peibl', 'Pina', 'Shi', 'Tito', 'Tomimi']


class Player:
    def __init__(self, player_id: int, joystick: Joystick = NullJoystick(), keyboard: Keyboard = NullKeyboard):
        self.driver = None
        self.id = player_id

        self.img = player_id % len(sprites)
        self.char: Character = None
        self.restart_char()

        self.joystick: Joystick = joystick
        self.keyboard = keyboard

    def set_driver(self, driver):
        self.driver = driver

    def actions(self, events, pressed):
        # controles presionados
        if self.joystick.hold_up() or self.keyboard.hold_up(pressed):
            self.driver.hold_up(self)
        if self.joystick.hold_down() or self.keyboard.hold_down(pressed):
            self.driver.hold_down(self)
        if self.joystick.hold_left() or self.keyboard.hold_left(pressed):
            self.driver.hold_left(self)
        if self.joystick.hold_right() or self.keyboard.hold_right(pressed):
            self.driver.hold_right(self)

        # controles pulsados
        if self.joystick.press_up() or self.keyboard.press_up(events):
            self.driver.press_up(self)
        if self.joystick.press_down() or self.keyboard.press_down(events):
            self.driver.press_down(self)
        if self.joystick.press_left() or self.keyboard.press_left(events):
            self.driver.press_left(self)
        if self.joystick.press_right() or self.keyboard.press_right(events):
            self.driver.press_right(self)

        if self.joystick.press_primary() or self.keyboard.press_primary(events):
            self.driver.press_primary(self)
        if self.joystick.press_secondary() or self.keyboard.press_secondary(events):
            self.driver.press_secondary(self)
        if self.joystick.press_start() or self.keyboard.press_start(events):
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
                              x=100 + 50 * self.id, y=200)
        return
