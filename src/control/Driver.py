from typing import List

import pygame

from src.control.Joystick import init_joystick
from src.control.Keyboard import Player1Keyboard, Player2Keyboard
from src.control.Player import Player
from src.control.GameState import GameState, InMainMenu, InGame, InCharSelect, InStartScreen, Paused, GameWon, \
    GameOver
from src.elements.Level import load_level
from src.elements.Sound import stop_background
from src.utils import path
from settings.Game import FPS


class Driver:
    def __init__(self, screen: pygame.Surface):
        self.players: List[Player] = []

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

    def add_player(self, player):
        self.players.append(player)
        player.set_driver(self)
        return

    def remove_player(self, player):
        self.players.remove(player)

        for p in self.players:
            if p.id > player.id:
                p.id -= 1
        return

    def used_joysticks(self):
        used = set()
        for player in self.players:
            used.add(player.joystick.get_id())
        return used

    def available_joysticks(self):
        joysticks = []
        for i in range(pygame.joystick.get_count()):
            if i not in self.used_joysticks():
                joysticks.append(init_joystick(i))
        return joysticks

    def available_keyboards(self):
        player1 = True
        player2 = True
        for player in self.players:
            player1 &= not player.keyboard.is_player_one()
            player2 &= not player.keyboard.is_player_two()

        keyboards = []
        if player1:
            keyboards.append(Player1Keyboard())
        if player2:
            keyboards.append(Player2Keyboard())
        return keyboards

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

    def press_primary(self, player: Player):
        self.state.press_primary(player)
        return

    def press_secondary(self, player: Player):
        self.state.press_secondary(player)
        return

    def press_start(self, player: Player):
        self.state.press_start(player)
        return

    # ----------- control del juego -------------

    def reset_game(self):
        self.players = []
        self.set_state(InStartScreen(self))
        return

    def main_menu(self):
        stop_background()
        self.set_state(InMainMenu(self))
        return

    def char_select(self):
        self.set_state(InCharSelect(self))

    def start_game(self):
        from src.elements.Level import load_level2
        from static.maps.level1 import level1

        levels = [
            load_level2(level1),
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
        self.running = False
        return
