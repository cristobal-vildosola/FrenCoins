from typing import List

from settings.GUI import TITLE_COLOR, SUBTITLE_COLOR, MENU_BACKGROUND
from src.control.Keyboard import Player1Keyboard
from src.control.Player import Player
from src.elements.Group import CustomGroup
from src.elements.Level import Level
from src.elements.Sound import jump_sound, hit_sound, play_background, stop_background
from src.menu.Menu import Menu, CharSelectMenu
from src.menu.MenuHandler import *
from src.menu.MenuItem import Button, MenuText


class GameState:
    def __init__(self, driver):
        self.driver = driver

    def tick(self, events):
        pass

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

    def press_primary(self, player: Player):
        pass

    def press_secondary(self, player: Player):
        pass


class MenuState(GameState):
    def __init__(self, driver, menu: Menu):
        super().__init__(driver)
        self.menu: Menu = menu

    def tick(self, events):
        self.driver.screen.fill(MENU_BACKGROUND)
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

    def press_primary(self, player: Player):
        self.menu.select(player)
        return

    def press_secondary(self, player: Player):
        self.menu.unselect(player)
        return

    def press_start(self, player: Player):
        self.menu.start(player)
        return


class InStartScreen(MenuState):
    def __init__(self, driver):
        items = [
            MenuText(text="FrenCoins", size=120, color=TITLE_COLOR),
            MenuText(text="Press START / ENTER", size=40),
        ]
        super().__init__(driver, Menu(driver, items))

    def tick(self, events):
        super().tick(events)

        # detectar control jugador 1
        for joystick in self.driver.available_joysticks():
            if joystick.hold_start():
                player = Player(len(self.driver.players), joystick=joystick)
                self.driver.add_player(player)
                self.driver.main_menu()

        # permitir solo teclado jugador 1
        keyboard = Player1Keyboard()
        if keyboard.press_primary(events):
            player = Player(len(self.driver.players), keyboard=keyboard)
            self.driver.add_player(player)
            self.driver.main_menu()
        return


class InMainMenu(MenuState):
    def __init__(self, driver):
        items = [
            MenuText(text="FrenCoins", size=100, color=TITLE_COLOR),
            Button(handler=CharSelect(driver), text="Start Game"),
            Button(handler=MainMenuHandler(driver), text="Instructions"),
            Button(handler=QuitGame(driver), text="Exit", color=(170, 0, 0), hover_color=(220, 0, 0)),
        ]
        super().__init__(driver, Menu(driver, items))

    def press_secondary(self, player: Player):
        self.driver.reset_game()
        return


class InCharSelect(MenuState):
    def __init__(self, driver):
        super().__init__(driver, CharSelectMenu(driver))

    def tick(self, events):
        super().tick(events)

        # detectar conección de nuevos controles
        for joystick in self.driver.available_joysticks():
            if joystick.hold_start():
                player = Player(len(self.driver.players), joystick=joystick)
                self.add_player(player)

        # detectar teclado
        for keyboard in self.driver.available_keyboards():
            if keyboard.press_primary(events):
                player = Player(len(self.driver.players), keyboard=keyboard)
                self.add_player(player)
        return

    def add_player(self, player):
        self.driver.add_player(player)
        self.menu.add_player(self.driver.players[-1])
        return


class InGame(GameState):
    def __init__(self, driver, levels: List[Level]):
        super().__init__(driver)

        play_background()
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
        self.driver.pause(self)
        return

    def press_primary(self, player: Player):
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
                    self.driver.game_won(level)
                else:
                    self.driver.game_over(level)

        if len(chars) == 0:
            self.driver.game_over(level)

        return


class Paused(MenuState):
    def __init__(self, driver, prev_state: InGame):
        items = [
            MenuText("Pause", size=100, color=SUBTITLE_COLOR),
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
        self.background.set_alpha(150)

    def tick(self, events):
        self.prev_state.levels[self.prev_state.level_num].draw(self.driver.screen)
        self.driver.screen.blit(self.background, (0, 0))
        self.menu.draw(self.driver.screen)
        return

    def press_secondary(self, player: Player):
        self.unpause()
        return

    def press_start(self, player: Player):
        self.unpause()
        return

    def unpause(self):
        self.driver.unpause(self.prev_state)
        return


class GameOver(MenuState):
    def __init__(self, driver, level):
        items = [
            MenuText(text="Game Over", size=100, color=(200, 10, 10)),
            MenuText(text="Press START to go back to Main Menu", size=40, color=SUBTITLE_COLOR),
        ]
        super().__init__(driver, Menu(driver, items))
        self.level = level

    def tick(self, events):
        self.level.draw(self.driver.screen)
        self.menu.draw(self.driver.screen)
        return

    def press_start(self, player: Player):
        self.driver.main_menu()
        stop_background()
        return


class GameWon(MenuState):
    def __init__(self, driver, level: Level):
        items = [
            MenuText(text="Congratules!", size=100, color=TITLE_COLOR),
            MenuText(text="Press START to go back to Main Menu", size=40, color=SUBTITLE_COLOR),
        ]
        super().__init__(driver, Menu(driver, items))

        self.level = level
        self.chars = CustomGroup()
        for player in self.driver.players:
            self.chars.add(player.char)

        jump_sound.set_volume(0)
        hit_sound.set_volume(0)

    def tick(self, events):
        for char in self.chars:
            char.jump()

        self.chars.update()
        self.level.detect_collisions(self.chars)

        self.level.draw(self.driver.screen)
        self.chars.draw(self.driver.screen)
        self.menu.draw(self.driver.screen)
        return

    def press_start(self, player: Player):
        jump_sound.set_volume(1)
        hit_sound.set_volume(1)
        stop_background()
        self.driver.main_menu()
        return
