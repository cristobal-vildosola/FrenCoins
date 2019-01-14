import pygame


class CustomGroup(pygame.sprite.Group):

    def __init__(self, *sprites):
        super().__init__(*sprites)

    def draw(self, surface):
        for sprite in self.sprites():
            sprite.draw(surface)
        return

    def detect_collisions(self, *groups, dokill=False):
        for group in groups:
            for sprite in self.sprites():
                sprite.detect_collisions(group, dokill)
        return

    def detect_impacts(self, *groups, dokill=True):
        for group in groups:
            for sprite in self.sprites():
                sprite.detect_impacts(group, dokill)
        return

    def detect_objectives(self, *groups):
        for group in groups:
            for sprite in self.sprites():
                sprite.detect_objectives(group)
