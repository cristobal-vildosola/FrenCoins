from pygame.locals import *


class Keyboard:
    def __init__(self, k_up=K_UP, k_down=K_DOWN, k_left=K_LEFT, k_right=K_RIGHT, k_primary=K_RETURN,
                 k_secondary=K_BACKSPACE, k_start=K_ESCAPE):
        self.k_up = k_up
        self.k_down = k_down
        self.k_left = k_left
        self.k_right = k_right
        self.k_primary = k_primary
        self.k_secondary = k_secondary
        self.k_start = k_start

    def hold_up(self, pressed):
        return pressed[self.k_up]

    def hold_down(self, pressed):
        return pressed[self.k_down]

    def hold_left(self, pressed):
        return pressed[self.k_left]

    def hold_right(self, pressed):
        return pressed[self.k_right]

    @staticmethod
    def has_keydown(key, events):
        for event in events:
            if event.type == KEYDOWN and event.key == key:
                return True
        return False

    def press_up(self, events):
        return self.has_keydown(self.k_up, events)

    def press_down(self, events):
        return self.has_keydown(self.k_down, events)

    def press_left(self, events):
        return self.has_keydown(self.k_left, events)

    def press_right(self, events):
        return self.has_keydown(self.k_right, events)

    def press_primary(self, events):
        return self.has_keydown(self.k_primary, events)

    def press_secondary(self, events):
        return self.has_keydown(self.k_secondary, events)

    def press_start(self, events):
        return self.has_keydown(self.k_start, events)

    def is_player_one(self):
        return False

    def is_player_two(self):
        return False

    def prymary_key(self):
        return ""


class NullKeyboard(Keyboard):
    def __init__(self):
        super().__init__(k_up=-1, k_down=-1, k_left=-1, k_right=-1, k_primary=-1, k_secondary=-1, k_start=-1)


class Player1Keyboard(Keyboard):
    def is_player_one(self):
        return True

    def prymary_key(self):
        return "ENTER"


class Player2Keyboard(Keyboard):
    def __init__(self):
        super().__init__(k_up=K_w, k_down=K_s, k_left=K_a, k_right=K_d, k_primary=K_e, k_secondary=K_q, k_start=-1)

    def is_player_two(self):
        return True

    def prymary_key(self):
        return "E"
