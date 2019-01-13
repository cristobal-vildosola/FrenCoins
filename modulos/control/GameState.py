from modulos.control.Player import Player
from modulos.menu.Menu import Menu, PauseMenu, MainMenu, CharSelectMenu
from modulos.elements.Level import Level
from modulos.elements.Group import CustomGroup

from typing import List


class GameState:
    def __init__(self, driver):
        self.driver = driver

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


class InMenu(GameState):
    def __init__(self, driver, menu: Menu):
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
        self.menu.action_left(player)
        return

    def press_right(self, player: Player):
        self.menu.action_right(player)
        return

    def press_main(self, player: Player):
        self.menu.select(player)
        return


class Paused(InMenu):
    def __init__(self, driver, prev_state: GameState):
        super().__init__(driver, PauseMenu(driver))
        self.prev_state = prev_state

        # oscurecer juego
        self.background = self.driver.screen.copy()
        self.background.fill((0, 0, 0))
        self.background.set_alpha(150)  # TODO: setting darkness
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


class InMainMenu(InMenu):
    def __init__(self, driver):
        super().__init__(driver, MainMenu(driver))


class InGame(GameState):
    def __init__(self, driver, levels: List[Level]):
        super().__init__(driver)

        # TODO: reproducir música
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


class InCharSelect(InMenu):
    def __init__(self, driver):
        super().__init__(driver, CharSelectMenu(driver))

    def tick(self):
        super().tick()
        # detectar conección de nuevos controles
        return
