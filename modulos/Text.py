import pygame

# los fonts se tienen que inicializar, para no hacerlo cada vez que
# creo un nuevo texto los guardo en un diccionario según tamaño
fonts = {}


class Text:

    def __init__(self, text, x, y, color=(0, 0, 0), height=30, center=False, antialias=True):
        global fonts
        if height not in fonts:
            fonts[height] = pygame.font.Font("static/freesansbold.ttf", height)

        self.text = fonts[height].render(text, antialias, color)

        if center:
            self.pos = self.text.get_rect()
            self.pos.center = (x, y)
        else:
            self.pos = self.text.get_rect().move(x, y)

    def draw(self, screen):
        screen.blit(self.text, self.pos)
        return
