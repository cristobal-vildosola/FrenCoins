from typing import List

import pygame

from modulos.Text import Text
from modulos.MenuHandlers import *


class MenuItem:

    def action_right(self):
        pass

    def action_left(self):
        pass

    def select(self):
        pass

    def draw(self, screen, x, y, selected=False):
        pass

    def get_height(self):
        return 0

    @staticmethod
    def is_selectable():
        return True


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
        total_height = 0
        for item in self.menu_items:
            total_height += item.get_height()

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


class Button(MenuItem):

    def __init__(self, handler, text, width=0, height=30,
                 color=(17, 76, 170), hover_color=(59, 133, 249), text_color=(215, 215, 215)):
        self.handler = handler

        self.text = Text(text, color=text_color, height=height)

        self.color = color
        self.hover_color = hover_color

        self.height = height * 2
        self.width = max(width, self.text.pos.right + height)
        self.background = pygame.Surface([self.width, self.height])

    def select(self):
        self.handler.handle()

    def draw(self, screen, x, y, selected=False):
        if selected:
            self.background.fill(self.hover_color)
        else:
            self.background.fill(self.color)

        screen.blit(self.background, (x - self.width / 2, y))

        self.text.set_pos(x, y + self.height / 2, center=True)
        self.text.draw(screen)
        return

    def get_height(self):
        return self.height


class MenuText(MenuItem):

    def __init__(self, text, height=30, color=(0, 0, 0)):
        self.text = Text(text, color=color, height=height)
        self.height = height

    @staticmethod
    def is_selectable():
        return False

    def draw(self, screen, x, y, selected=False):
        self.text.set_pos(x, y + self.height / 2, center=True)
        self.text.draw(screen)
        return

    def get_height(self):
        return self.height


class PauseMenu(Menu):
    def __init__(self, driver):
        items = [
            MenuText("Pause", height=100, color=(217, 217, 14)),
            Button(handler=None, text="Continue"),
            Button(handler=MainMenuHandler(driver), text="Main Menu"),
        ]
        super().__init__(driver, items)


class MainMenu(Menu):
    def __init__(self, driver):
        items = [
            MenuText(text="FrenCoins", height=100, color=(14, 117, 14)),
            Button(handler=StartGame(driver), text="Start!"),
            Button(handler=QuitGame(driver), text="Exit", color=(170, 0, 0), hover_color=(220, 0, 0))
        ]
        super().__init__(driver, items)
