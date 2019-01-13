from typing import List

from modulos.menu.MenuHandler import *
from modulos.menu.MenuItem import *


class Menu:

    def __init__(self, driver, menu_items=(), x=400, screen_height=600, padding=20):
        self.driver = driver
        self.menu_items: List[MenuItem] = menu_items
        self.selected = 0
        if len(menu_items) > 0:
            self.ensure_selectable(self.select_next)

        self.x = x
        self.screen_height = screen_height
        self.padding = padding

    def add_item(self, item: MenuItem):
        self.menu_items.append(item)
        return

    def draw(self, screen):
        total_height = - self.padding
        for item in self.menu_items:
            total_height += item.get_height() + self.padding

        y = self.screen_height / 2 - total_height / 2

        for i in range(len(self.menu_items)):
            item = self.menu_items[i]

            item.draw(screen, self.x, y, selected=self.selected == i)
            y += item.get_height() + self.padding

        return

    def select_next(self):
        self.selected = (self.selected + 1) % len(self.menu_items)
        self.ensure_selectable(self.select_next)
        return

    def select_previous(self):
        self.selected = (self.selected - 1) % len(self.menu_items)
        self.ensure_selectable(self.select_previous)
        return

    def ensure_selectable(self, next_item):
        current = self.selected

        while not self.menu_items[self.selected].is_selectable():
            next_item()

            if current == self.selected:
                break
        return

    def action_right(self):
        self.menu_items[self.selected].action_right()

    def action_left(self):
        self.menu_items[self.selected].action_left()

    def select(self):
        self.menu_items[self.selected].select()


class PauseMenu(Menu):
    def __init__(self, driver):
        items = [
            MenuText("Pause", height=100, color=(217, 217, 217)),
            Button(handler=ContinueGame(driver), text="Continue"),
            Button(handler=StartGame(driver), text="Restart"),
            Button(handler=MainMenuHandler(driver), text="Main Menu"),
            Button(handler=QuitGame(driver), text="Exit", color=(170, 0, 0), hover_color=(220, 0, 0)),
        ]
        super().__init__(driver, items)


class MainMenu(Menu):
    def __init__(self, driver):
        items = [
            MenuText(text="FrenCoins", height=100, color=(14, 117, 14)),
            Button(handler=StartGame(driver), text="Start!"),
            Button(handler=QuitGame(driver), text="Exit", color=(170, 0, 0), hover_color=(220, 0, 0)),
        ]
        super().__init__(driver, items)
