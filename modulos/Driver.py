import pygame
from modulos.Menu import Menu, PauseMenu, MainMenu
from modulos.Level import Level, load_level
from modulos.Characters import Player, CustomGroup
from modulos.utils import path

from typing import List


class Driver:
    def __init__(self, players: List[Player], screen: pygame.Surface):
        self.players: List[Player] = players
        for player in players:
            player.set_driver(self)

        self.screen: pygame.Surface = screen

        self.state: State = MainMenuState(self)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.fps: int = 60  # TODO: constant

        self.running = True

    def set_state(self, state):
        self.state = state
        return

    def tick(self):
        pressed = pygame.key.get_pressed()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
                return

        for player in self.players:
            player.actions(events, pressed)

        if self.running:
            self.state.tick()
            self.clock.tick(self.fps)
            pygame.display.flip()

        return

    def add_player(self, player: Player):
        self.players.append(player)
        return

    def action_up(self, player: Player):
        self.state.action_up(player)
        return

    def action_down(self, player: Player):
        self.state.action_down(player)
        return

    def action_left(self, player: Player):
        self.state.action_left(player)
        return

    def action_right(self, player: Player):
        self.state.action_right(player)
        return

    def action_start(self, player: Player):
        self.state.action_start(player)
        return

    def action_main(self, player: Player):
        self.state.action_main(player)
        return

    def start_game(self):
        levels = [
            load_level(path('static/maps/level1.json')),
            load_level(path('static/maps/level2.json')),
            load_level(path('static/maps/level3.json')),
            load_level(path('static/maps/level4.json')),
            load_level(path('static/maps/level5.json')),
        ]
        self.set_state(InGame(self, levels))
        return

    def main_menu(self):
        self.set_state(MainMenuState(self))
        return

    def quit_game(self):
        pygame.quit()
        self.running = False
        return


class State:
    def __init__(self, driver: Driver):
        self.driver: Driver = driver

    def tick(self):
        pass

    def set_state(self, state):
        self.driver.set_state(state)
        return

    def action_up(self, player: Player):
        pass

    def action_down(self, player: Player):
        pass

    def action_left(self, player: Player):
        pass

    def action_right(self, player: Player):
        pass

    def action_start(self, player: Player):
        pass

    def action_main(self, player: Player):
        pass


class MenuState(State):
    def __init__(self, driver: Driver, menu: Menu):
        super().__init__(driver)
        self.menu: Menu = menu

    def tick(self):
        self.driver.screen.fill((226, 205, 86))
        self.menu.draw(self.driver.screen)
        return

    def action_up(self, player: Player):
        self.menu.select_previous()
        return

    def action_down(self, player: Player):
        self.menu.select_next()
        return

    def action_left(self, player: Player):
        self.menu.action_left()
        return

    def action_right(self, player: Player):
        self.menu.action_right()
        return

    def action_main(self, player: Player):
        self.menu.select()
        return


class Paused(MenuState):
    def __init__(self, driver: Driver, prev_state: State):
        super().__init__(driver, PauseMenu(driver))
        self.prev_state = prev_state

        self.background = self.driver.screen.copy()
        self.background.fill((0, 0, 0))
        self.background.set_alpha(100)
        self.driver.screen.blit(self.background, (0, 0))

    def tick(self):
        self.menu.draw(self.driver.screen)
        return

    def action_start(self, player: Player):
        self.set_state(self.prev_state)
        return


class MainMenuState(MenuState):
    def __init__(self, driver):
        super().__init__(driver, MainMenu(driver))


class InGame(State):
    def __init__(self, driver: Driver, levels: List[Level]):
        super().__init__(driver)

        self.levels: List[Level] = levels
        self.level_num = 0
        self.level = self.levels[self.level_num]

        self.chars = CustomGroup()
        for player in self.driver.players:
            self.chars.add(player.char)

    def tick(self):
        chars = self.chars
        level = self.levels[self.level_num]

        # mov automático
        chars.update()
        level.update()

        # colisiones
        level.detect_collisions(chars)

        # terminar ronda
        if level.is_over(chars):

            level.end(chars)
            self.level_num += 1

            if self.level_num >= len(self.levels):
                # TODO terminar juego, estado GameWon
                self.set_state(MainMenuState(self.driver))

        if len(chars) == 0:
            # TODO terminar juego, estado GameOver
            self.set_state(MainMenuState(self.driver))

        # dibujar
        self.driver.screen.fill((25, 115, 200))
        level.draw(self.driver.screen)
        chars.draw(self.driver.screen)
        pass

    def action_up(self, player: Player):
        player.char.jump()
        return

    def action_down(self, player: Player):
        player.char.fall()
        return

    def action_left(self, player: Player):
        player.char.move_left()
        return

    def action_right(self, player: Player):
        player.char.move_right()
        return

    def action_start(self, player: Player):
        self.set_state(Paused(self.driver, self))
        return

    def action_main(self, player: Player):
        player.char.jump()
        return
