import pygame

from modulos.utils import path

pygame.mixer.init()
pygame.mixer.set_num_channels(12)
channels = [
    pygame.mixer.Channel(0),  # player1 jump
    pygame.mixer.Channel(1),  # player2 jump
    pygame.mixer.Channel(2),  # player3 jump
    pygame.mixer.Channel(3),  # player4 jump
    pygame.mixer.Channel(4),  # player1 hit
    pygame.mixer.Channel(5),  # player2 hit
    pygame.mixer.Channel(6),  # player3 hit
    pygame.mixer.Channel(7),  # player4 hit
    pygame.mixer.Channel(8),  # cannons
    pygame.mixer.Channel(9),  # coins
    pygame.mixer.Channel(10),  # fondo
    pygame.mixer.Channel(11),  #
]

jump_sound = pygame.mixer.Sound(path("static/sounds/ha.wav"))
hit_sound = pygame.mixer.Sound(path("static/sounds/ah.wav"))
fire_sound = pygame.mixer.Sound(path("static/sounds/pium.wav"))
coin_sound = pygame.mixer.Sound(path("static/sounds/prim.wav"))
background_sound = pygame.mixer.Sound(path("static/sounds/mii2.wav"))


def play_jump(player_id):
    channels[player_id % 4].play(jump_sound)
    return


def play_hit(player_id):
    channels[player_id % 4 + 4].play(hit_sound)
    return


def play_fire():
    channels[8].play(fire_sound)
    return


def play_coin():
    channels[9].play(coin_sound)
    return


def play_background():
    channels[10].play(background_sound, loops=-1)
    return


def stop_background():
    channels[10].stop()
    return
