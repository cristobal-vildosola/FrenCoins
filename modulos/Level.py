import pygame
from modulos.Text import Text
from modulos.Characters import CustomGroup
from modulos.utils import path


class Level:

    def __init__(self, duration, objectives, cannons, blocks, platforms, fps=60):
        self.time = duration
        self.prep_time = 3
        self.fps = fps

        self.objectives = objectives

        self.blocks = blocks
        self.platforms = platforms

        self.cannons = cannons
        self.bullets = CustomGroup()
        for cannon in cannons:
            cannon.set_bullet_group(self.bullets)

    def update(self):
        if self.prep_time > 0:
            self.prep_time -= 1.0 / self.fps
            return

        self.time -= 1.0 / self.fps

        self.cannons.update()
        self.bullets.update()
        return

    def detect_collisions(self, chars):
        chars.detect_collisions(self.blocks)
        chars.detect_collisions(self.platforms)
        chars.detect_collisions(self.cannons)

        for _ in chars:
            chars.detect_collisions(chars)

        self.blocks.detect_impacts(self.bullets)
        chars.detect_impacts(self.bullets)

        # no se pueden agarrar objetivos durante la preparación
        if self.prep_time <= 0:
            chars.detect_objectives(self.objectives)

        return

    def draw(self, screen):

        self.blocks.draw(screen)
        self.platforms.draw(screen)

        number_color = (200, 200, 200)
        if self.time < 5:
            number_color = (255, 0, 0)
        Text(str(round(self.time, 1)), 400, 16, number_color, center=True, height=30).draw(screen)

        self.cannons.draw(screen)

        # no se pueden agarrar objetivos durante la preparación
        if self.prep_time <= 0:
            for objective in self.objectives:
                objective.draw(screen)
        else:
            # mostrar tiempo de preparación
            Text(str(int(self.prep_time) + 1), 400, 300, (200, 200, 200), center=True,
                 height=int(80 + self.prep_time % 1 * 60)).draw(screen)

        self.bullets.draw(screen)
        return

    def is_over(self, characters):
        if self.time <= 0:
            return True

        for char in characters:
            if len(char.objectives) < len(self.objectives):
                return False

        return True

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
        self.image = pygame.image.load(path('static/img/FrenCoin.png'))
        self.image = pygame.transform.smoothscale(self.image, (50, 50))

        self.rect = self.image.get_rect().move(pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        return
