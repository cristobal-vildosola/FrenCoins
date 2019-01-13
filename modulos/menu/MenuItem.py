import pygame
from modulos.elements.Text import Text


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
    padding = 20  # TODO: settings
    margin = 20

    def __init__(self, handler, text, width=200, height=30,
                 color=(17, 76, 170), hover_color=(59, 133, 249), text_color=(215, 215, 215)):
        # TODO: settings colors
        self.handler = handler
        self.text = Text(text, color=text_color, height=height)

        self.height = height + 2 * self.padding
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

    def __init__(self, text, height=30, color=(0, 0, 0), margin=20):
        self.text = Text(text, color=color, height=height)
        self.height = height
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
    inner_padding = 5
    outer_padding = 10

    triangle_size = 20
    char_size = 100  # TODO: setting

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
        pygame.draw.polygon(screen, (255, 255, 255),
                            [(x + pad + triangle_size * 0.86, y),
                             (x + pad + triangle_size * 0.86, y + triangle_size),
                             (x + pad, y + triangle_size / 2)])

        # rigth
        pygame.draw.polygon(screen, (255, 255, 255),
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

        Text("Press", x=x + self.width / 2, y=y + self.height / 2 - 25, height=25,
             color=(200, 200, 200), center=True).draw(screen)
        Text("START", x=x + self.width / 2, y=y + self.height / 2, height=25,
             color=(200, 200, 200), center=True).draw(screen)
        Text("to join", x=x + self.width / 2, y=y + self.height / 2 + 25, height=25,
             color=(200, 200, 200), center=True).draw(screen)
        return


class MultiCharSelect(MenuItem):
    padding = 20  # TODO: settings
    margin = 20

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
