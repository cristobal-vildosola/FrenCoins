import os

import pygame
from pygame.locals import *

from modulos.LevelLoader import load_level
from modulos.Characters import Character, CustomGroup
from modulos.Joystick import XBoxJoystick
from modulos.Sounds import play_background, jump_sound
from modulos.Text import Text
from modulos.utils import path
from modulos.Menu import Menu, Button, MenuText


def play(screen, players, clock, fps):
    chars = CustomGroup(players)
    screen_width, screen_height = 800, 600

    # niveles
    levels = [
        load_level(path('static/maps/level1.json')),
        load_level(path('static/maps/level2.json')),
        load_level(path('static/maps/level3.json')),
        load_level(path('static/maps/level4.json')),
        load_level(path('static/maps/level5.json')),
    ]

    level_num = 0
    level = levels[level_num]

    play_background()
    jump_sound.set_volume(1)
    running = True
    while running:

        # eventos
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                return

        # acciones de personajes
        pressed = pygame.key.get_pressed()
        for char in chars:
            char.actions(events, pressed)

        # mov automático
        chars.update()
        level.update()

        # colisiones
        level.detect_collisions(chars)

        # terminar ronda
        if level.is_over(chars):

            level.end(chars)
            level_num += 1

            if level_num >= len(levels):
                running = False
            else:
                level = levels[level_num]

        if len(chars) == 0:
            running = False

        # dibujar
        screen.fill((25, 115, 200))
        level.draw(screen)
        chars.draw(screen)

        # actualizar y esperar un tick
        pygame.display.flip()
        clock.tick(fps)

    # pantalla final
    texto = "Game Over"
    color_texto = (230, 0, 0)
    if len(chars) > 0:
        texto = "Congratules!"
        color_texto = (0, 230, 0)

    titulo = Text(texto, screen_width / 2, screen_height / 2,
                  height=100, color=color_texto, center=True)
    subtitulo = Text("Presiona espacio o START para empezar de nuevo", screen_width / 2, screen_height / 2 + 100,
                     height=27, color=(255, 255, 255), center=True)

    jump_sound.set_volume(0)

    running = True
    while running:

        # eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    play(screen, players, clock, fps)
                    running = False

        for char in players:
            if char.joystick.start_press():
                play(screen, players, clock, fps)

        chars.update()
        chars.detect_collisions(levels[0].blocks)

        for char in chars:
            char.jump()

        # dibujar
        screen.fill((25, 115, 200))

        levels[0].blocks.draw(screen)
        chars.draw(screen)

        titulo.draw(screen)
        subtitulo.draw(screen)

        # actualizar y esperar un tick
        pygame.display.flip()
        clock.tick(fps)

    return


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60

    # centrar ventana
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("FrenCoins")
    pygame.display.set_icon(pygame.image.load(path('static/img/favicon.png')))

    # personajes
    player1 = Character(0, x=600, y=200, img=path('static/img/Pina.png'),
                        k_up=K_UP, k_left=K_LEFT, k_down=K_DOWN, k_right=K_RIGHT)
    player2 = Character(1, x=500, y=100, img=path('static/img/Tito.png'),
                        k_up=K_w, k_left=K_a, k_down=K_s, k_right=K_d)
    player3 = Character(2, x=100, y=350, img=path('static/img/Shi.png'),
                        k_up=K_i, k_left=K_j, k_down=K_k, k_right=K_l)
    player4 = Character(3, x=300, y=200, img=path('static/img/FatCow.png'),
                        k_up=K_t, k_left=K_f, k_down=K_g, k_right=K_h)

    chars = [player1, player2]

    # controles
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        print(joystick.get_name())
        if joystick.get_name().lower().rfind("xbox") != -1:
            joysticks.append(XBoxJoystick(joystick))

            if i < len(chars):
                chars[i].joystick = joysticks[i]

    menu = Menu([MenuText(text="FrenCoins", height=100, color=(14, 117, 14)),
                 Button(handler=None, text="Empezar juego"),
                 Button(handler=None, text="Salir", color=(170, 0, 0), hover_color=(220, 0, 0))])

    running = True
    while running:

        # eventos
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.select_next()
                if event.key == K_DOWN:
                    menu.select_previous()
                if event.key == K_RETURN:
                    running = False

        screen.fill((226, 205, 86))
        menu.draw(screen)

        # actualizar y esperar un tick
        pygame.display.flip()
        clock.tick(fps)

    play(screen, chars, clock, fps)

    pygame.quit()
    return


if __name__ == "__main__":
    main()
