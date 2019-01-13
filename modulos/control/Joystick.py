class Joystick:
    def __init__(self, joystick, main_button=0, start_button=7,
                 x_axis=0, y_axis=1, x_orientation=1, y_orientation=1, x_treshold=0.5, y_treshold=0.7):
        self.joystick = joystick

        self.start_button = start_button
        self.main_button = main_button

        self.start_pressed = 0
        self.main_pressed = 0
        self.prev_x_value = 0
        self.prev_y_value = 0

        self.x_treshold = x_treshold
        self.x_axis = x_axis
        self.x_orientation = x_orientation
        self.y_treshold = y_treshold
        self.y_axis = y_axis
        self.y_orientation = y_orientation

    def update(self):
        self.main_pressed = self.hold_main()
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

    def hold_main(self):
        return self.joystick.get_button(self.main_button)

    def hold_start(self):
        return self.joystick.get_button(self.start_button)

    def press_main(self):
        return not self.main_pressed and self.hold_main()

    def press_start(self):
        return not self.start_pressed and self.hold_start()


class XBoxJoystick(Joystick):
    def __init__(self, joystick):
        Joystick.__init__(self, joystick, main_button=0, start_button=7,
                          x_axis=0, y_axis=1, x_orientation=1, y_orientation=-1)


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

    def hold_main(self):
        return False

    def hold_start(self):
        return False

    def press_main(self):
        return False

    def press_start(self):
        return False
