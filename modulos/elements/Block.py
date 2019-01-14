import pygame


class Block(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y, color=(60, 30, 0)):
        # TODO settings color
        super().__init__()

        # imagen a mostrar cada vez que se llama draw()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # posición
        self.rect = self.image.get_rect().move(x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return

    # choque con el lado izquierdo
    def collide_left(self, moving_sprite):
        if moving_sprite.old_rect.right <= self.rect.left:
            moving_sprite.rect.right = self.rect.left
            return True
        return False

    # choque con el lado derecho
    def collide_right(self, moving_sprite):
        if moving_sprite.old_rect.left >= self.rect.right:
            moving_sprite.rect.left = self.rect.right
            return True
        return False

    # choque con el lado superior
    def collide_top(self, moving_sprite):
        if moving_sprite.old_rect.bottom <= self.rect.top:
            moving_sprite.rect.bottom = self.rect.top
            return True
        return False

    # choque con el lado inferior
    def collide_bottom(self, moving_sprite):
        if moving_sprite.old_rect.top >= self.rect.bottom:
            moving_sprite.rect.top = self.rect.bottom
            return True
        return False

    def detect_impacts(self, group, dokill=True):
        pygame.sprite.spritecollide(self, group, dokill=dokill)
        return


class Platform(Block):

    def __init__(self, width, height, x, y, color=(100, 10, 100)):
        # TODO settings color
        super().__init__(width, height, x, y, color)

    # choque con el lado izquierdo, no hace nada
    def collide_left(self, moving_sprite):
        return False

    # choque con el lado derecho, no hace nada
    def collide_right(self, moving_sprite):
        return False

    # choque con el lado inferior, no hace nada
    def collide_bottom(self, moving_sprite):
        return False

    def collide_top(self, moving_sprite):
        if moving_sprite.falling:
            return False
        return Block.collide_top(self, moving_sprite)
