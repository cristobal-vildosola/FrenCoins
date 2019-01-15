import pygame

from settings.GUI import BUTTON_MARGIN, BUTTON_PADDING, BUTTON_TEXT_COLOR, BUTTON_HOVER_COLOR, BUTTON_COLOR, \
    BUTTON_WIDTH, SELECT_MARGIN, SELECT_PADDING, SELECT_INNER_PADDING, SELECT_OUTER_PADDING, SELECT_CHAR_SIZE, \
    SELECT_TRIANGLE_SIZE, SELECT_TRIANGLE_COLOR, TEXT_MARGIN, SCREEN_WIDTH
from src.elements.Text import Text


class MenuItem:

    def action_right(self, player):
        pass

    def action_left(self, player):
        pass

    def select(self, player):
        pass

    def unselect(self, player):
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
        self.width = max(width, self.text.rect.right + 2 * self.padding)

        self.background = pygame.Surface([self.width, self.height])
        self.color = color
        self.hover_color = hover_color

    def select(self, player):
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
        self.locked = False

    def action_right(self):
        if not self.locked:
            self.player.next_char()
        return

    def action_left(self):
        if not self.locked:
            self.player.prev_char()
        return

    def select(self):
        self.locked = True
        return

    def unselect(self):
        self.locked = False
        return

    def draw(self, screen, x, y):
        self.draw_box(screen, x, y)

        # mover esquina
        x += self.outer_padding
        y += self.outer_padding
        self.draw_char(screen, x, y)

        y += self.char_size + self.inner_padding
        if self.locked:
            self.draw_check(screen, x, y)
        else:
            self.draw_arrows(screen, x, y)

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

    def draw_check(self, screen, x, y):
        char_size = self.char_size
        triangle_size = self.triangle_size

        pygame.draw.lines(screen, (10, 235, 10), False,
                          [(x + char_size / 2 - triangle_size / 2, y + triangle_size / 2),
                           (x + char_size / 2, y + triangle_size),
                           (x + char_size / 2 + triangle_size, y)], int(self.triangle_size / 5))
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


class OpenCharSelect(CharSelect):
    def __init__(self):
        super().__init__(None)
        self.locked = True

        size = int(self.char_size / 4)
        self.text1 = Text("Press", size=size, color=BUTTON_TEXT_COLOR)
        self.text2 = Text("START", size=size, color=BUTTON_TEXT_COLOR)
        self.text3 = Text("to join", size=size, color=BUTTON_TEXT_COLOR)

    def draw(self, screen, x, y):
        self.draw_box(screen, x, y)

        size = int(self.char_size / 4)
        self.text1.set_pos(x=x + self.width / 2, y=y + self.height / 2 - size, center=True)
        self.text2.set_pos(x=x + self.width / 2, y=y + self.height / 2, center=True)
        self.text3.set_pos(x=x + self.width / 2, y=y + self.height / 2 + size, center=True)

        self.text1.draw(screen)
        self.text2.draw(screen)
        self.text3.draw(screen)
        return

    def action_right(self):
        return

    def action_left(self):
        return

    def select(self):
        return

    def unselect(self):
        return


class MultiCharSelect(MenuItem):
    padding = SELECT_PADDING
    margin = SELECT_MARGIN
    max_select_per_row = int(SCREEN_WIDTH / (CharSelect.width + padding))

    def __init__(self, players):
        self.selects = []
        for player in players:
            self.selects.append(CharSelect(player))
        self.selects.append(OpenCharSelect())

        self.start_message = Text("Press START to begin the game")

    def add_player(self, player):
        self.selects.insert(-1, CharSelect(player))
        return

    def is_selectable(self):
        return True

    def is_ready(self):
        ready = True
        for character_select in self.selects:
            ready &= character_select.locked
        return ready

    def draw(self, screen, x, y, selected=False):
        select_width = CharSelect.width
        select_height = CharSelect.height
        rows = self.get_num_rows()

        for row in range(rows):
            selects_in_row = self.max_select_per_row

            # ultima fila
            if row == rows - 1:
                selects_in_row = int((len(self.selects) - 1) % self.max_select_per_row) + 1

            width = select_width * selects_in_row + self.padding * (selects_in_row - 1)
            current_x = x - width / 2

            for i in range(selects_in_row):
                character_select = self.selects[i + row * self.max_select_per_row]
                character_select.draw(screen, current_x, y)

                current_x += select_width + self.padding
            y += select_height + self.padding

        if self.is_ready():
            self.draw_start_message(screen, x, y)
        return

    def draw_start_message(self, screen, x, y):
        self.start_message.set_pos(x - self.start_message.rect.width / 2, y)
        self.start_message.draw(screen)
        return

    def get_num_rows(self):
        return int((len(self.selects) - 1) / self.max_select_per_row) + 1

    def get_height(self):
        return CharSelect.height * self.get_num_rows() + self.padding * (self.get_num_rows() - 1)

    def get_margin(self):
        return self.margin

    def action_right(self, player):
        self.selects[player.id].action_right()
        return

    def action_left(self, player):
        self.selects[player.id].action_left()
        return

    def select(self, player):
        self.selects[player.id].select()
        return

    def unselect(self, player):
        self.selects[player.id].unselect()
        return
