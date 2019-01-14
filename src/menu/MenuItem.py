import pygame

from src.elements.Text import Text
from settings.GUI import BUTTON_MARGIN, BUTTON_PADDING, BUTTON_TEXT_COLOR, BUTTON_HOVER_COLOR, BUTTON_COLOR, \
    BUTTON_WIDTH, SELECT_MARGIN, SELECT_PADDING, SELECT_INNER_PADDING, SELECT_OUTER_PADDING, SELECT_CHAR_SIZE, \
    SELECT_TRIANGLE_SIZE, SELECT_TRIANGLE_COLOR, TEXT_MARGIN


class MenuItem:

    def action_right(self):
        pass

    def action_left(self):
        pass

    def select(self):
        pass

    def draw(self, screen, x, y, selected=False):
        pass

    def get_height(self):
        pass

    def get_margin(self):
        pass

    @staticmethod
    def is_selectable():
        return True


class Button(MenuItem):
    padding = BUTTON_PADDING
    margin = BUTTON_MARGIN

    def __init__(self, handler, text, width=BUTTON_WIDTH, text_size=30,
                 color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=BUTTON_TEXT_COLOR):
        self.handler = handler
        self.text = Text(text, color=text_color, size=text_size)

        self.height = text_size + 2 * self.padding
        self.width = max(width, self.text.pos.right + 2 * self.padding)

        self.background = pygame.Surface([self.width, self.height])
        self.color = color
        self.hover_color = hover_color

    def select(self):
        self.handler.handle()

    def draw(self, screen, x, y, selected=False):
        if selected:
            self.background.fill(self.hover_color)
        else:
            self.background.fill(self.color)

        screen.blit(self.background, (x - self.width / 2, y))

        self.text.set_pos(x, y + self.height / 2, center=True)
        self.text.draw(screen)
        return

    def get_height(self):
        return self.height

    def get_margin(self):
        return self.margin


class MenuText(MenuItem):

    def __init__(self, text, size=30, color=(0, 0, 0), margin=TEXT_MARGIN):
        self.text = Text(text, color=color, size=size)
        self.height = size
        self.margin = margin

    @staticmethod
    def is_selectable():
        return False

    def draw(self, screen, x, y, selected=False):
        self.text.set_pos(x, y + self.height / 2, center=True)
        self.text.draw(screen)
        return

    def get_height(self):
        return self.height

    def get_margin(self):
        return self.margin


class CharSelect:
    inner_padding = SELECT_INNER_PADDING
    outer_padding = SELECT_OUTER_PADDING

    triangle_size = SELECT_TRIANGLE_SIZE
    char_size = SELECT_CHAR_SIZE

    width = char_size + 2 * outer_padding
    height = char_size + 2 * outer_padding + triangle_size + inner_padding

    def __init__(self, player):
        self.player = player

    def draw(self, screen, x, y):
        self.draw_box(screen, x, y)

        # mover esquina por outer_padding
        x = x + self.outer_padding
        y = y + self.outer_padding

        self.draw_char(screen, x, y)
        self.draw_arrows(screen, x, y + self.char_size + self.inner_padding)
        return

    def draw_box(self, screen, x, y):
        box = pygame.Surface((self.width, self.height))
        box.fill((0, 0, 0))
        box.set_alpha(150)
        screen.blit(box, (x, y))
        return

    def draw_char(self, screen, x, y):
        image = pygame.image.load(self.player.img_path())
        image = pygame.transform.smoothscale(image, (self.char_size, self.char_size))
        screen.blit(image, (x, y))
        return

    def draw_arrows(self, screen, x, y):
        char_size = self.char_size
        triangle_size = self.triangle_size
        pad = self.inner_padding

        # left
        pygame.draw.polygon(screen, SELECT_TRIANGLE_COLOR,
                            [(x + pad + triangle_size * 0.86, y),
                             (x + pad + triangle_size * 0.86, y + triangle_size),
                             (x + pad, y + triangle_size / 2)])

        # rigth
        pygame.draw.polygon(screen, SELECT_TRIANGLE_COLOR,
                            [(x + char_size - pad - triangle_size * 0.86, y),
                             (x + char_size - pad - triangle_size * 0.86, y + triangle_size),
                             (x + char_size - pad, y + triangle_size / 2)])
        return

    def get_width(self):
        return self.width

    def get_heigth(self):
        return self.height

    def draw_open_space(self, screen, x, y):
        self.draw_box(screen, x, y)

        size = int(self.char_size / 4)
        Text("Press", x=x + self.width / 2, y=y + self.height / 2 - size, size=size,
             color=BUTTON_TEXT_COLOR, center=True).draw(screen)
        Text("START", x=x + self.width / 2, y=y + self.height / 2, size=size,
             color=BUTTON_TEXT_COLOR, center=True).draw(screen)
        Text("to join", x=x + self.width / 2, y=y + self.height / 2 + size, size=size,
             color=BUTTON_TEXT_COLOR, center=True).draw(screen)
        return


class MultiCharSelect(MenuItem):
    padding = SELECT_PADDING
    margin = SELECT_MARGIN

    def __init__(self, players):
        self.selects = []
        for player in players:
            self.selects.append(CharSelect(player))

    def add_player(self, player):
        self.selects.append(CharSelect(player))
        return

    def is_selectable(self):
        return False

    def draw(self, screen, x, y, selected=False):
        width = self.selects[0].get_width() * (len(self.selects) + 1) + self.padding * (len(self.selects))

        x = x - width / 2
        for character_select in self.selects:
            character_select.draw(screen, x, y)
            x += character_select.get_width() + self.padding

        self.selects[0].draw_open_space(screen, x, y)
        return

    def get_height(self):
        return self.selects[0].get_heigth()

    def get_margin(self):
        return self.margin
