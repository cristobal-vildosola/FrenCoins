from typing import List

import pygame

from src.control.Player import Player
from src.control.GameState import GameState, InMainMenu, InGame, InCharSelect, InStartScreen, Paused, GameWon, \
    GameOver
from src.elements.Level import load_level
from src.utils import path
from settings.GUI import FPS


class Driver:
    def __init__(self, screen: pygame.Surface):
        self.players: List[Player] = []
        self.used_joysticks = set()

        self.screen: pygame.Surface = screen

        self.state: GameState = InStartScreen(self)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.fps: int = FPS

        self.running = True

    def tick(self):
        pressed = pygame.key.get_pressed()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()

        for player in self.players:
            player.actions(events, pressed)

        self.state.tick(events)

        self.clock.tick(self.fps)
        pygame.display.flip()
        return

    def set_state(self, state):
        self.state = state
        return

    def add_player(self, joystick):
        self.players.append(Player(len(self.players), driver=self, joystick=joystick))
        self.used_joysticks.add(joystick.get_id())
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

    def main_menu(self):
        self.set_state(InMainMenu(self))
        return

    def char_select(self):
        self.set_state(InCharSelect(self))

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

    def pause(self, prev_state):
        self.set_state(Paused(self, prev_state))
        return

    def unpause(self, prev_state):
        self.set_state(prev_state)
        return

    def game_won(self, level):
        self.set_state(GameWon(self, level))

    def game_over(self, level):
        self.set_state(GameOver(self, level))

    def quit_game(self):
        pygame.quit()
        self.running = False
        exit(0)
        return
