import pygame

from src.utils import path
from settings.GUI import COIN_SIZE


class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(path('static/img/FrenCoin.png'))
        self.image = pygame.transform.smoothscale(self.image, (COIN_SIZE, COIN_SIZE))

        self.rect = self.image.get_rect().move((x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return
