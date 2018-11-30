import pygame


class Char(pygame.sprite.Sprite):
    """
    Personaje base, permite detectar colisiones con otros sprites.
    """

    def __init__(self, width, height, x, y, img):
        """
        :param width: ancho del personake
        :param height: alto del personaje
        :param x: posición en eje x
        :param y: posición en eje y
        :param img: imagen del personaje
        """
        pygame.sprite.Sprite.__init__(self)

        # imagen a mostrar cada vez que se llama draw()
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))

        # posición
        self.rect = self.image.get_rect().move(x, y)
        self.old_rect = self.rect.copy()

    def move(self, dx=0, dy=0):
        self.rect.move_ip(dx, dy)
        return

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.old_rect = self.rect.copy()
        return

    def detect_collisions(self, group, dokill=False):
        collisions = pygame.sprite.spritecollide(self, group, dokill=dokill)

        for sprite in collisions:
            self.collide(sprite)
        return

    def collide(self, sprite):
        dx = self.rect.x - self.old_rect.x
        dy = self.rect.y - self.old_rect.y

        if dx > 0:  # choque hacia la derecha
            sprite.collide_left(self)

        elif dx < 0:  # choque hacia la izquierda
            sprite.collide_right(self)

        if dy > 0:  # choque hacia abajo
            sprite.collide_top(self)

        elif dy < 0:  # choque hacia arriba
            sprite.collide_bottom(self)

        return

    # choque con el lado izquierdo
    def collide_left(self, moving_sprite):
        if moving_sprite.old_rect.right <= self.old_rect.left:
            middle = (moving_sprite.old_rect.right + self.old_rect.left) / 2
            moving_sprite.rect.right = middle
            return True
        return False

    # choque con el lado derecho
    def collide_right(self, moving_sprite):
        if moving_sprite.old_rect.left >= self.old_rect.right:
            middle = (moving_sprite.old_rect.left + self.old_rect.right) / 2
            moving_sprite.rect.left = middle
            return True
        return False

    # choque con el lado superior
    def collide_top(self, moving_sprite):
        if moving_sprite.old_rect.bottom <= self.old_rect.top:
            middle = (moving_sprite.old_rect.bottom + self.old_rect.top) / 2
            moving_sprite.rect.bottom = middle
            return True
        return False

    # choque con el lado inferior
    def collide_bottom(self, moving_sprite):
        if moving_sprite.old_rect.top >= self.old_rect.bottom:
            middle = int((moving_sprite.old_rect.top + self.old_rect.bottom) / 2)
            moving_sprite.rect.top = middle
            return True
        return False


class GravityChar(Char):
    """
    Agrega gravedad y saltos al personaje, se modifica collide para actualizar standing y vy al chocar
    """

    def __init__(self, width, height, x, y, img, g=1, jumpspeed=15):
        """
        :param g: gravidad a aplicar en cada ciclo, para valores menores a 1 no funciona bien.
        :param jumpspeed: velocidad en x al momento de saltar
        """
        Char.__init__(self, width, height, x, y, img)

        self.g = g
        self.jumpspeed = jumpspeed
        self.vy = 0
        self.standing = False

    def update(self):
        self.vy += self.g
        self.move(0, self.vy)
        self.standing = False

    def jump(self):
        if self.standing:
            self.vy = -self.jumpspeed
            self.standing = False
        return

    def collide(self, sprite):
        dx = self.rect.x - self.old_rect.x
        dy = self.rect.y - self.old_rect.y

        if dx > 0:  # choque hacia la derecha
            sprite.collide_left(self)

        elif dx < 0:  # choque hacia la izquierda
            sprite.collide_right(self)

        if dy > 0:  # choque hacia abajo
            if sprite.collide_top(self):
                self.vy = 0
                self.standing = True

        elif dy < 0:  # choque hacia arriba
            if sprite.collide_bottom(self):
                self.vy = 0

        return


class CustomGroup(pygame.sprite.Group):
    """
    Permite manejar los caracteres para usar su propio método draw (que actualiza la posición anterior)
    y la detección de colisiones.
    """

    def __init__(self, *sprites):
        pygame.sprite.Group.__init__(self, *sprites)

    def draw(self, surface):
        for sprite in self.sprites():
            self.spritedict[sprite] = sprite.draw(surface)
        return

    def detect_collisions(self, *groups, dokill=False):
        """
        Detecta las colisiones entre cada objeto del grup y los grupos entregados

        :param groups:
        :param dokill: determina si se eliminan los sprites con los que se choca.
        """
        for group in groups:
            for sprite in self.sprites():
                sprite.detect_collisions(group, dokill)
        return
