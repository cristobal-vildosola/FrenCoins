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
        return 0

    @staticmethod
    def is_selectable():
        return True


class Button(MenuItem):

    def __init__(self, handler, text, width=0, height=30,
                 color=(17, 76, 170), hover_color=(59, 133, 249), text_color=(215, 215, 215)):
        self.handler = handler

        self.text = Text(text, color=text_color, height=height)

        self.color = color
        self.hover_color = hover_color

        self.height = height * 2
        self.width = max(width, self.text.pos.right + height)
        self.background = pygame.Surface([self.width, self.height])

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


class MenuText(MenuItem):

    def __init__(self, text, height=30, color=(0, 0, 0)):
        self.text = Text(text, color=color, height=height)
        self.height = height

    @staticmethod
    def is_selectable():
        return False

    def draw(self, screen, x, y, selected=False):
        self.text.set_pos(x, y + self.height / 2, center=True)
        self.text.draw(screen)
        return

    def get_height(self):
        return self.height
