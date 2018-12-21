class Joystick:
    def __init__(self, joystick, a_button=0, start_button=7,
                 x_axis=0, y_axis=1, x_orientation=1, y_orientation=1, treshold=0.4):
        self.joystick = joystick

        self.start_button = start_button

        self.a_button = a_button
        self.a_pressed = 0

        self.treshold = treshold
        self.x_axis = x_axis
        self.x_orientation = x_orientation
        self.y_axis = y_axis
        self.y_orientation = y_orientation

    def right(self):
        return self.x_orientation * self.joystick.get_axis(self.x_axis) > self.treshold

    def left(self):
        return self.x_orientation * -self.joystick.get_axis(self.x_axis) > self.treshold

    def up(self):
        return self.y_orientation * self.joystick.get_axis(self.y_axis) > self.treshold

    def down(self):
        return self.y_orientation * -self.joystick.get_axis(self.y_axis) > self.treshold

    def start_press(self):
        return self.joystick.get_button(self.start_button)

    def a_press(self):
        if self.joystick.get_button(self.a_button):

            if not self.a_pressed:
                self.a_pressed = 1
                return True

            self.a_pressed = 1

        else:
            self.a_pressed = 0
        return False


class XBoxJoystick(Joystick):
    def __init__(self, joy_id):
        Joystick.__init__(self, joy_id, a_button=0, start_button=7,
                          x_axis=0, y_axis=1, x_orientation=1, y_orientation=-1)
