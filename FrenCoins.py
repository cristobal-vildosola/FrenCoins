import os

import pygame
from pygame.locals import *

from LevelLoader import load_level
from modulos.Characters import GravityChar, CustomGroup
from modulos.Joystick import XBoxJoystick
from modulos.Sounds import play_background, jump_sound
from modulos.Text import Text
from modulos.utils import path

# centrar ventana
os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("FrenCoins")
    pygame.display.set_icon(pygame.image.load(path('static/img/favicon.png')))

    # personajes
    player1 = GravityChar(0, 600, 200, img=path('static/img/Ardila.png'))
    player2 = GravityChar(1, 100, 350, img=path('static/img/Checho.png'))
    player3 = GravityChar(3, 500, 100, img=path('static/img/Tito.png'))
    player4 = GravityChar(2, 300, 200, img=path('static/img/FatCow.png'))

    chars = CustomGroup([player1, player2, player3])
    chars_static = [player1, player2, player3, player4]  # lista para asociar con joysticks

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

    # controles
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        print(joystick.get_name())
        if joystick.get_name().lower().rfind("xbox") != -1:
            joysticks.append(XBoxJoystick(joystick))

    play_background()
    jump_sound.set_volume(1)
    running = True
    while running:

        # eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    player1.jump()
                if event.key == K_w:
                    player2.jump()
                if event.key == K_i:
                    player3.jump()
                if event.key == K_t:
                    player4.jump()

        # joysticks
        for i in range(len(joysticks)):
            if i < len(chars_static):
                if joysticks[i].right():
                    chars_static[i].move_right()
                if joysticks[i].left():
                    chars_static[i].move_left()
                if joysticks[i].down():
                    chars_static[i].fall()
                if joysticks[i].a_press():
                    chars_static[i].jump()

        # teclas apretadas
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            player1.move_left()
        if pressed[K_RIGHT]:
            player1.move_right()
        if pressed[K_DOWN]:
            player1.fall()

        if pressed[K_a]:
            player2.move_left()
        if pressed[K_d]:
            player2.move_right()
        if pressed[K_s]:
            player2.fall()

        if pressed[K_j]:
            player3.move_left()
        if pressed[K_l]:
            player3.move_right()
        if pressed[K_k]:
            player3.fall()

        if pressed[K_f]:
            player4.move_left()
        if pressed[K_h]:
            player4.move_right()
        if pressed[K_g]:
            player4.fall()

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
                pygame.quit()
                return

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    main()
                    return

        for i in range(len(joysticks)):
            if i < len(chars_static):
                if joysticks[i].start_press():
                    main()
                    return

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

    pygame.quit()
    return


if __name__ == "__main__":
    main()
