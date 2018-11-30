import pygame

from Blocks import Block


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


class Cannon(Block):

    def __init__(self, x, y, bullet_group, frecuencia=60,
                 bullet_vx=6, bullet_vy=0, bullet_radius=5, bullet_damage=10):
        pygame.sprite.Sprite.__init__(self)

        # posición
        self.image = pygame.image.load('img/cannon.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(x, y)

        # para lanzar proyectiles
        self.bullet_group = bullet_group
        self.frecuencia = frecuencia
        self.iteracion = 0

        # propiedades de balas
        self.bullet_vx = bullet_vx
        self.bullet_vy = bullet_vy
        self.bullet_radius = bullet_radius
        self.bullet_damage = bullet_damage

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, *args):
        self.iteracion += 1

        if self.iteracion == self.frecuencia:
            # disparar bala
            self.bullet_group.add(
                Bullet(self.bullet_radius, self.rect.center[0], self.rect.center[1],
                       self.bullet_vx, self.bullet_vy, self.bullet_damage)
            )
            self.iteracion = 0
