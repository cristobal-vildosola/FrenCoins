import pygame


class Joystick:
    def __init__(self, joystick: pygame.joystick.Joystick, primary_button=0, secondary_button=1, start_button=7,
                 x_axis=0, y_axis=1, x_orientation=1, y_orientation=1, x_treshold=0.5, y_treshold=0.7):
        self.joystick: pygame.joystick.Joystick = joystick

        self.primary_button = primary_button
        self.secondary_button = secondary_button
        self.start_button = start_button

        self.primary_pressed = 0
        self.secondary_pressed = 0
        self.start_pressed = 0
        self.prev_x_value = 0
        self.prev_y_value = 0

        self.x_treshold = x_treshold
        self.x_axis = x_axis
        self.x_orientation = x_orientation
        self.y_treshold = y_treshold
        self.y_axis = y_axis
        self.y_orientation = y_orientation

    def update(self):
        self.primary_pressed = self.hold_primary()
        self.secondary_pressed = self.hold_secondary()
        self.start_pressed = self.hold_start()
        self.prev_x_value = self.joystick.get_axis(self.x_axis)
        self.prev_y_value = self.joystick.get_axis(self.y_axis)
        return

    def hold_up(self):
        return self.y_orientation * self.joystick.get_axis(self.y_axis) > self.y_treshold

    def hold_down(self):
        return -self.y_orientation * self.joystick.get_axis(self.y_axis) > self.y_treshold

    def hold_left(self):
        return -self.x_orientation * self.joystick.get_axis(self.x_axis) > self.x_treshold

    def hold_right(self):
        return self.x_orientation * self.joystick.get_axis(self.x_axis) > self.x_treshold

    def press_up(self):
        return self.y_orientation * self.prev_y_value <= self.y_treshold and self.hold_up()

    def press_down(self):
        return -self.y_orientation * self.prev_y_value <= self.y_treshold and self.hold_down()

    def press_left(self):
        return -self.x_orientation * self.prev_x_value <= self.x_treshold and self.hold_left()

    def press_right(self):
        return self.x_orientation * self.prev_x_value <= self.x_treshold and self.hold_right()

    def hold_primary(self):
        return self.joystick.get_button(self.primary_button)

    def press_primary(self):
        return not self.primary_pressed and self.hold_primary()

    def hold_secondary(self):
        return self.joystick.get_button(self.secondary_button)

    def press_secondary(self):
        return not self.secondary_pressed and self.hold_secondary()

    def hold_start(self):
        return self.joystick.get_button(self.start_button)

    def press_start(self):
        return not self.start_pressed and self.hold_start()

    def get_id(self):
        return self.joystick.get_id()


class NullJoystick(Joystick):

    def __init__(self):
        super().__init__(None)

    def update(self):
        return

    def hold_up(self):
        return False

    def hold_down(self):
        return False

    def hold_left(self):
        return False

    def hold_right(self):
        return False

    def press_up(self):
        return False

    def press_down(self):
        return False

    def press_left(self):
        return False

    def press_right(self):
        return False

    def hold_primary(self):
        return False

    def press_primary(self):
        return False

    def hold_secondary(self):
        return False

    def press_secondary(self):
        return False

    def hold_start(self):
        return False

    def press_start(self):
        return False

    def get_id(self):
        return -1


class XBoxJoystick(Joystick):
    def __init__(self, joystick):
        Joystick.__init__(self, joystick, primary_button=0, start_button=7,
                          x_axis=0, y_axis=1, x_orientation=1, y_orientation=-1)


class USBJoystick(Joystick):
    def __init__(self, joystick):
        Joystick.__init__(self, joystick, primary_button=2, start_button=9,
                          x_axis=0, y_axis=1, x_orientation=1, y_orientation=-1)


def init_joystick(joy_id: int):
    joystick = pygame.joystick.Joystick(joy_id)
    joystick.init()

    if joystick.get_name().lower().rfind("xbox") != -1:
        return XBoxJoystick(joystick)

    if joystick.get_name().lower().rfind("usb") != -1:
        return USBJoystick(joystick)

    return Joystick(joystick)
