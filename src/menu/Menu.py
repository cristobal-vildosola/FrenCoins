from typing import List

from settings.GUI import SCREEN_HEIGHT, SCREEN_WIDTH, TITLE_COLOR
from src.menu.MenuHandler import *
from src.menu.MenuItem import MenuItem, Button, MenuText, MultiCharSelect


class Menu:

    def __init__(self, driver, menu_items=(), x=SCREEN_WIDTH / 2):
        self.driver = driver
        self.menu_items: List[MenuItem] = menu_items
        self.selected = 0
        if len(menu_items) > 0:
            self.ensure_selectable()

        self.x = x

    def add_item(self, item: MenuItem):
        self.menu_items.append(item)
        return

    def draw(self, screen):
        total_height = 0
        for item in self.menu_items:
            total_height += item.get_height() + item.get_margin()
        total_height -= self.menu_items[-1].get_margin()

        y = SCREEN_HEIGHT / 2 - total_height / 2

        for i in range(len(self.menu_items)):
            item = self.menu_items[i]

            item.draw(screen, self.x, y, selected=self.selected == i)
            y += item.get_height() + item.get_margin()

        return

    def select_next(self):
        self.selected = (self.selected + 1) % len(self.menu_items)
        self.ensure_selectable()
        return

    def select_previous(self):
        self.selected = (self.selected - 1) % len(self.menu_items)
        self.ensure_selectable(direction=-1)
        return

    def ensure_selectable(self, direction=1):
        current = self.selected

        while not self.menu_items[self.selected].is_selectable():
            self.selected = (self.selected + direction) % len(self.menu_items)

            if current == self.selected:
                break
        return

    def action_right(self, player):
        self.menu_items[self.selected].action_right(player)

    def action_left(self, player):
        self.menu_items[self.selected].action_left(player)

    def select(self, player):
        self.menu_items[self.selected].select(player)
        return

    def unselect(self, player):
        self.menu_items[self.selected].unselect(player)
        return

    def start(self, player):
        pass

    def add_player(self, player):
        pass


class CharSelectMenu(Menu):
    def __init__(self, driver):
        self.char_select = MultiCharSelect(driver.players)
        self.start_game = StartGame(driver)
        items = [
            MenuText(text="Choose your character", size=60, color=TITLE_COLOR),
            self.char_select,
        ]
        super().__init__(driver, items)

    def add_player(self, player):
        self.char_select.add_player(player)
        return

    def start(self, player):
        if self.char_select.is_ready():
            self.start_game.handle()
        return
