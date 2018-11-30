import pygame


class Char(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y, img, max_life=100):
        pygame.sprite.Sprite.__init__(self)

        # imagen a mostrar cada vez que se llama draw()
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))

        # posición
        self.width = width
        self.height = height
        self.rect = self.image.get_rect().move(x, y)
        self.old_rect = self.rect.copy()

        # vida
        self.max_life = max_life
        self.life = max_life

        self.life_frame = pygame.Surface([width, 4])
        self.life_frame.fill((255, 0, 0))
        self.life_bar = pygame.Surface([width, 4])
        self.life_bar.fill((0, 255, 0))

        # objetivos
        self.objectives = set()

    def move(self, dx=0, dy=0):
        self.rect.move_ip(dx, dy)
        return

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        self.draw_life(screen)
        self.draw_objectives(screen)

        self.old_rect = self.rect.copy()
        return

    def draw_life(self, screen):
        screen.blit(self.life_frame, self.rect.move(0, -10))
        current_width = int(self.width * self.life / self.max_life)
        screen.blit(pygame.transform.smoothscale(self.life_bar, (current_width, 4)),
                    self.rect.move(0, -10))
        return

    def draw_objectives(self, screen):
        if len(self.objectives) > 0:
            img = list(self.objectives)[0].image.copy()
            img = pygame.transform.smoothscale(img, (10, 10))

            for i in range(len(self.objectives)):
                screen.blit(img, self.rect.move(2, 2 + 12 * i).topright)
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

    def detect_impacts(self, group, dokill=True):
        collisions = pygame.sprite.spritecollide(self, group, dokill=dokill)

        for sprite in collisions:
            self.impact(sprite)
        return

    def impact(self, sprite):
        sprite.impact(self)

        if self.life <= 0:
            self.kill()
        return

    def detect_objectives(self, group):
        collisions = pygame.sprite.spritecollide(self, group, dokill=False)

        for sprite in collisions:
            self.get_objective(sprite)

    def get_objective(self, objective):
        self.objectives.add(objective)
        return

    def clear_objectives(self):
        self.objectives.clear()
        return


class GravityChar(Char):

    def __init__(self, width, height, x, y, img, g=1, jumpspeed=15):
        Char.__init__(self, width, height, x, y, img)

        self.g = g
        self.jumpspeed = jumpspeed
        self.vy = 0

        self.jumptries = 0
        self.maxjumptries = 5
        self.standing = False

    def update(self):
        if self.standing and self.jumptries > 0:
            self.vy = -self.jumpspeed
            self.standing = False

        self.jumptries -= 1
        self.vy += self.g
        self.rect.y += self.vy
        self.standing = False

    def jump(self):
        if self.standing:
            self.vy = -self.jumpspeed
            self.standing = False
        else:
            self.jumptries = self.maxjumptries

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


class Kirby(GravityChar):

    def __init__(self, width, height, x, y, img, g=0.5, jumpspeed=8, max_jumps=3):
        GravityChar.__init__(self, width, height, x, y, img, g, jumpspeed)

        self.max_jumps = max_jumps
        self.jumps = max_jumps

    def jump(self):
        if self.jumps > 0:
            self.vy = -self.jumpspeed
            self.jumps -= 1

        return

    def draw(self, screen):
        img = self.image.copy()
        rect = self.rect.copy()

        if self.vy < 0:
            infl = (-self.vy) ** 0.5
            rect = rect.inflate(infl * 3, infl)
            img = pygame.transform.smoothscale(img, rect.size)

        screen.blit(img, rect.topleft)

        self.draw_life(screen)
        self.draw_objectives(screen)

        self.old_rect = self.rect.copy()
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
                self.jumps = self.max_jumps

        elif dy < 0:  # choque hacia arriba
            if sprite.collide_bottom(self):
                self.vy = 0

        return


class CustomGroup(pygame.sprite.Group):

    def __init__(self, *sprites):
        pygame.sprite.Group.__init__(self, *sprites)

    def draw(self, surface):
        for sprite in self.sprites():
            self.spritedict[sprite] = sprite.draw(surface)
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
