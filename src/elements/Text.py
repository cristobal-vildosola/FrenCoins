import pygame

from src.utils import path

# los fonts se tienen que inicializar, para no hacerlo cada vez que
# creo un nuevo texto los guardo en un diccionario según tamaño
fonts = {}


class Text:

    def __init__(self, text, x=0, y=0, color=(0, 0, 0), size=30, center=False, antialias=True):
        global fonts
        if size not in fonts:
            fonts[size] = pygame.font.Font(path("static/freesansbold.ttf"), size)

        self.text = fonts[size].render(text, antialias, color)

        self.pos = self.text.get_rect()
        self.set_pos(x, y, center)

    def draw(self, screen):
        screen.blit(self.text, self.pos)
        return

    def set_pos(self, x, y, center=False):
        if center:
            self.pos.center = (x, y)
        else:
            self.pos.topleft = (x, y)
        return