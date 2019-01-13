import pygame

from modulos.utils import path


class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path('static/img/FrenCoin.png'))
        self.image = pygame.transform.smoothscale(self.image, (50, 50))

        self.rect = self.image.get_rect().move((x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return
