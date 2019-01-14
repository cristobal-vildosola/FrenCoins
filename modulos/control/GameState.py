from typing import List

import pygame

from modulos.control.Joystick import init_joystick, NullJoystick
from modulos.control.Player import Player
from modulos.elements.Group import CustomGroup
from modulos.elements.Level import Level
from modulos.menu.Menu import Menu, CharSelectMenu
from modulos.menu.MenuItem import Button, MenuText
from modulos.menu.MenuHandler import *


class GameState:
    def __init__(self, driver):
        self.driver = driver

    def tick(self, events):
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


class MenuState(GameState):
    def __init__(self, driver, menu: Menu):
        super().__init__(driver)
        self.menu: Menu = menu

    def tick(self, events):
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


class InStartScreen(MenuState):
    def __init__(self, driver):
        items = [
            MenuText(text="FrenCoins", height=120, color=(14, 117, 14)),
            MenuText(text="Press START / ENTER to begin", height=40),
        ]
        super().__init__(driver, Menu(driver, items))

    def tick(self, events):
        super().tick(events)

        # detectar control jugador 1
        for i in range(pygame.joystick.get_count()):
            joystick = init_joystick(i)

            if joystick.hold_start():
                self.driver.add_player(joystick)
                self.set_state(InMainMenu(self.driver))

        # detectar teclado
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.driver.add_player(NullJoystick())
                    self.set_state(InMainMenu(self.driver))
        return


class InMainMenu(MenuState):
    def __init__(self, driver):
        items = [
            MenuText(text="FrenCoins", height=100, color=(14, 117, 14)),
            Button(handler=CharSelect(driver), text="Start Game"),
            Button(handler=MainMenuHandler(driver), text="Instructions"),
            Button(handler=QuitGame(driver), text="Exit", color=(170, 0, 0), hover_color=(220, 0, 0)),
        ]
        super().__init__(driver, Menu(driver, items))


class Paused(MenuState):
    def __init__(self, driver, prev_state: GameState):
        items = [
            MenuText("Pause", height=100, color=(217, 217, 217)),
            Button(handler=ContinueGame(driver), text="Continue"),
            Button(handler=StartGame(driver), text="Restart"),
            Button(handler=MainMenuHandler(driver), text="Main menu"),
            Button(handler=QuitGame(driver), text="Exit", color=(170, 0, 0), hover_color=(220, 0, 0)),
        ]
        super().__init__(driver, Menu(driver, items))

        self.prev_state = prev_state

        # oscurecer juego
        self.background = self.driver.screen.copy()
        self.background.fill((0, 0, 0))
        self.background.set_alpha(150)  # TODO: setting darkness
        self.driver.screen.blit(self.background, (0, 0))

    def tick(self, events):
        self.menu.draw(self.driver.screen)
        return

    def press_start(self, player: Player):
        self.unpause()
        return

    def unpause(self):
        self.set_state(self.prev_state)
        return


class InCharSelect(MenuState):
    def __init__(self, driver):
        super().__init__(driver, CharSelectMenu(driver))

    def tick(self, events):
        super().tick(events)

        # detectar conección de nuevos controles
        for i in range(pygame.joystick.get_count()):

            # ignorar controles ya conectados
            if i not in self.driver.used_joysticks:
                joystick = init_joystick(i)

                if joystick.hold_start():
                    self.driver.add_player(joystick)
                    self.menu.add_player(self.driver.players[-1])
        return


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

    def tick(self, events):
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
