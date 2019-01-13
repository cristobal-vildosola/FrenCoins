import pygame

from modulos.elements.Block import Block
from modulos.elements.Sound import play_fire
from modulos.utils import path
import math


class Cannon(Block):

    def __init__(self, x, y, frecuencia=60,
                 x_speed=0, y_speed=0, bullet_radius=5, bullet_damage=10, bullet_group=None):
        pygame.sprite.Sprite.__init__(self)

        # posición
        self.image = pygame.image.load(path('static/img/cannon.png'))
        # escalar a tamaño
        self.image = pygame.transform.smoothscale(self.image, (50, 50))
        # voltear horizontalmente
        self.image = pygame.transform.flip(self.image, x_speed < 0, False)

        # obtener rectángulo antes de rotar para evitar que cambie el tamaño para colisiones
        self.rect = self.image.get_rect().move(x, y)

        # rotar según angulo de disparo
        self.image = pygame.transform.rotate(self.image, -math.degrees(math.atan(y_speed / x_speed)))

        # obtener rect y corregir posición de dibujo
        self.pos = self.image.get_rect()
        self.pos.center = self.rect.center

        # para lanzar proyectiles
        self.bullet_group = bullet_group
        self.frecuencia = frecuencia
        self.iteracion = 0

        # propiedades de balas
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.bullet_radius = bullet_radius
        self.bullet_damage = bullet_damage

    def update(self, *args):
        self.iteracion += 1

        if self.iteracion == self.frecuencia:
            self.shoot()
            self.iteracion = 0
        return

    def draw(self, screen):
        screen.blit(self.image, self.pos)
        return

    def set_bullet_group(self, bullet_group):
        self.bullet_group = bullet_group
        return

    def shoot(self):
        self.bullet_group.add(
            Bullet(self.bullet_radius,
                   self.rect.center[0] - self.bullet_radius, self.rect.center[1] - self.bullet_radius,
                   self.x_speed, self.y_speed, self.bullet_damage))
        play_fire()
        return


class Bullet(pygame.sprite.Sprite):

    def __init__(self, radius, x, y, x_speed, y_speed, damage=10, color=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)

        # propiedades
        self.color = color
        self.radius = radius

        # posición
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)

        # velocidad
        self.vx = x_speed
        self.vy = y_speed

        # daño
        self.damage = damage

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
        return

    def update(self, *args):
        self.rect.move_ip(self.vx, self.vy)
        return

    def impact(self, sprite):
        sprite.life -= self.damage
        return
