import pygame
from Text import Text


class Level:

    def __init__(self, duration, objectives, fps=60, pos=(5, 5), color=(255, 255, 255)):
        self.time = duration
        self.fps = fps

        self.objectives = objectives

        self.pos = pygame.Rect(pos, (1, 1))
        self.color = color

    def update(self):
        self.time -= 1.0 / self.fps

    def draw(self, screen):
        time = Text(str(int(self.time)), self.pos.top, self.pos.left, self.color)
        time.draw(screen)

        for objective in self.objectives:
            objective.draw(screen)

    def is_over(self):
        return self.time <= 0

    def end(self, characters):
        for char in characters:

            if len(char.objectives) < len(self.objectives):
                char.kill()
            else:
                char.clear_objectives()
        return


class Objective(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/FrenCoin.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50, 50))

        self.rect = self.image.get_rect().move(pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
