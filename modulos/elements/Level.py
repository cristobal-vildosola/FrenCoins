import json

from modulos.elements.Block import Block, Platform
from modulos.elements.Cannon import Cannon
from modulos.elements.Coin import Coin
from modulos.elements.Group import CustomGroup
from modulos.elements.Text import Text


class Level:

    def __init__(self, duration=30,
                 coins=CustomGroup(), cannons=CustomGroup(), blocks=CustomGroup(), platforms=CustomGroup()):

        self.time = duration
        self.prep_time = 3
        self.fps = 60  # TODO: setting

        self.coins = coins

        self.blocks = blocks
        self.platforms = platforms

        self.cannons = cannons
        self.bullets = CustomGroup()
        for cannon in cannons:
            cannon.set_bullet_group(self.bullets)

        # TODO: settings level char positions

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
            chars.detect_objectives(self.coins)

        return

    def draw(self, screen):
        screen.fill((25, 115, 200))

        self.blocks.draw(screen)
        self.platforms.draw(screen)

        number_color = (200, 200, 200)  # TODO: setting
        if self.time < 5:
            number_color = (255, 0, 0)
        Text(str(round(self.time, 1)), x=400, y=16, color=number_color, center=True, height=30).draw(screen)

        self.cannons.draw(screen)

        # no se pueden agarrar objetivos durante la preparación
        if self.prep_time <= 0:
            for objective in self.coins:
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

        if len(self.coins) == 0:
            return False

        for char in characters:
            if len(char.objectives) < len(self.coins):
                return False

        return True

    def end(self, characters):
        for char in characters:

            if len(char.objectives) < len(self.coins):
                char.kill()

            else:
                char.clear_objectives()

        return


def load_level(level_json):
    with open(level_json) as f:
        level = json.load(f)

    blocks = CustomGroup()
    for block in level["blocks"]:
        blocks.add(Block(**block))

    platforms = CustomGroup()
    for platform in level["platforms"]:
        platforms.add(Platform(**platform))

    cannons = CustomGroup()
    for cannon in level["cannons"]:
        cannons.add(Cannon(**cannon))

    coins = CustomGroup()
    for coin in level["coins"]:
        coins.add(Coin(**coin))

    return Level(duration=level["duration"], coins=coins, cannons=cannons, blocks=blocks, platforms=platforms)
