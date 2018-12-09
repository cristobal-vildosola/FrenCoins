import pygame

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
]

jump_sound = pygame.mixer.Sound("static/sounds/")
hit_sound = pygame.mixer.Sound("static/sounds/")
fire_sound = pygame.mixer.Sound("static/sounds/")
coin_sound = pygame.mixer.Sound("static/sounds/")


def jump(player_id):
    channels[player_id].play(jump_sound)
    return


def hit(player_id):
    channels[player_id + 4].play(hit_sound)
    return


def fire():
    channels[8].play(fire_sound)
    return


def coin():
    channels[9].play(coin_sound)
    return
