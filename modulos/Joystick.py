import pygame


class Joystick:
    def __init__(self, joy_id, a_button=0, x_axis=0, y_axis=1):
        self.joystick = pygame.joystick.Joystick(joy_id)
        self.joystick.init()

        self.a_button = a_button
        self.a_pressed = 0

        self.treshold = 0.4
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.previus_y = 0

    def right(self):
        return self.joystick.get_axis(self.x_axis) > self.treshold

    def left(self):
        return self.joystick.get_axis(self.x_axis) < -self.treshold

    def down(self):
        return self.joystick.get_axis(self.y_axis) < -self.treshold

    def a_press(self):
        if self.joystick.get_button(0):
            if not self.a_pressed:
                return True
            self.a_pressed = 1

        else:
            self.a_pressed = 0

        return False


class XBoxJoystick(Joystick):
    def __init__(self, joy_id):
        Joystick.__init__(self, joy_id)
