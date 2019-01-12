import pygame
from modulos.Menu import Menu, PauseMenu, MainMenu
from modulos.Level import Level, load_level
from modulos.Players import Player, CustomGroup
from modulos.utils import path

from typing import List


class Driver:
    def __init__(self, players: List[Player], screen: pygame.Surface):
        self.players: List[Player] = players
        for player in players:
            player.set_driver(self)

        self.screen: pygame.Surface = screen

        self.state: State = InMainMenu(self)
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

    # ----------- acciones -------------

    def press_up(self, player: Player):
        self.state.press_up(player)
        return

    def press_down(self, player: Player):
        self.state.press_down(player)
        return

    def press_left(self, player: Player):
        self.state.press_left(player)
        return

    def press_right(self, player: Player):
        self.state.press_right(player)
        return

    def hold_up(self, player: Player):
        self.state.hold_up(player)
        return

    def hold_down(self, player: Player):
        self.state.hold_down(player)
        return

    def hold_left(self, player: Player):
        self.state.hold_left(player)
        return

    def hold_right(self, player: Player):
        self.state.hold_right(player)
        return

    def press_main(self, player: Player):
        self.state.press_main(player)
        return

    def press_start(self, player: Player):
        self.state.press_start(player)
        return

    # ----------- control del juego -------------

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
        self.set_state(InMainMenu(self))
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

    def press_up(self, player: Player):
        pass

    def press_down(self, player: Player):
        pass

    def press_left(self, player: Player):
        pass

    def press_right(self, player: Player):
        pass

    def hold_up(self, player: Player):
        pass

    def hold_down(self, player: Player):
        pass

    def hold_left(self, player: Player):
        pass

    def hold_right(self, player: Player):
        pass

    def press_start(self, player: Player):
        pass

    def press_main(self, player: Player):
        pass


class MenuState(State):
    def __init__(self, driver: Driver, menu: Menu):
        super().__init__(driver)
        self.menu: Menu = menu

    def tick(self):
        self.driver.screen.fill((226, 205, 86))
        self.menu.draw(self.driver.screen)
        return

    def press_up(self, player: Player):
        self.menu.select_previous()
        return

    def press_down(self, player: Player):
        self.menu.select_next()
        return

    def press_left(self, player: Player):
        self.menu.action_left()
        return

    def press_right(self, player: Player):
        self.menu.action_right()
        return

    def press_main(self, player: Player):
        self.menu.select()
        return


class Paused(MenuState):
    def __init__(self, driver: Driver, prev_state: State):
        super().__init__(driver, PauseMenu(driver))
        self.prev_state = prev_state

        # oscurecer juego
        self.background = self.driver.screen.copy()
        self.background.fill((0, 0, 0))
        self.background.set_alpha(150)
        self.driver.screen.blit(self.background, (0, 0))

    def tick(self):
        self.menu.draw(self.driver.screen)
        return

    def press_start(self, player: Player):
        self.unpause()
        return

    def unpause(self):
        self.set_state(self.prev_state)
        return


class InMainMenu(MenuState):
    def __init__(self, driver):
        super().__init__(driver, MainMenu(driver))

    def tick(self):
        super().tick()
        # detectar conección de nuevos controles
        return


class InGame(State):
    def __init__(self, driver: Driver, levels: List[Level]):
        super().__init__(driver)

        self.levels: List[Level] = levels
        self.level_num = 0

        self.chars = CustomGroup()
        for player in self.driver.players:
            player.restart_char()
            self.chars.add(player.char)

    def tick(self):
        chars = self.chars
        level = self.levels[self.level_num]

        # mov automático
        chars.update()
        level.update()

        # colisiones
        level.detect_collisions(chars)

        # terminar nivel
        self.check_level_end()

        # dibujar
        self.driver.screen.fill((25, 115, 200))
        level.draw(self.driver.screen)
        chars.draw(self.driver.screen)
        pass

    def press_up(self, player: Player):
        player.char.jump()
        return

    def hold_down(self, player: Player):
        player.char.fall()
        return

    def hold_left(self, player: Player):
        player.char.move_left()
        return

    def hold_right(self, player: Player):
        player.char.move_right()
        return

    def press_start(self, player: Player):
        self.set_state(Paused(self.driver, self))
        return

    def press_main(self, player: Player):
        player.char.jump()
        return

    def check_level_end(self):
        chars = self.chars
        level = self.levels[self.level_num]

        if level.is_over(chars):
            level.end(chars)
            self.level_num += 1

            if self.level_num >= len(self.levels):
                if len(chars) > 0:
                    # TODO terminar juego, estado GameWon
                    self.set_state(InMainMenu(self.driver))
                    return

                else:
                    # TODO terminar juego, estado GameOver
                    self.set_state(InMainMenu(self.driver))
                    return

        if len(chars) == 0:
            # TODO terminar juego, estado GameOver
            self.set_state(InMainMenu(self.driver))
            return

        return
