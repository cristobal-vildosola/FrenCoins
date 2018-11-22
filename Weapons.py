import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, radius, x, y, vx, vy, damage=10, color=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)

        # propiedades
        self.color = color
        self.radius = radius

        # posición
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)

        # velocidad
        self.vx = vx
        self.vy = vy

        # daño
        self.damage = damage

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def update(self, *args):
        self.rect.move_ip(self.vx, self.vy)

    def impact(self, sprite):
        sprite.life -= self.damage
        return
