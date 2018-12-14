import os

import pygame

from modulos.Blocks import Block, Platform
from modulos.Characters import GravityChar, CustomGroup
from modulos.Level import Level, Objective
from modulos.Sounds import play_background, jump_sound
from modulos.Text import Text
from modulos.Weapons import Cannon
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
    player1 = GravityChar(0, 600, 200, img=path('static/img/Checho.png'))
    player2 = GravityChar(1, 100, 350, img=path('static/img/Pina.png'))
    player3 = GravityChar(2, 300, 200, img=path('static/img/Peiblv3.png'))
    player4 = GravityChar(3, 500, 100, img=path('static/img/Tito.png'))

    chars = CustomGroup([player1, player2])
    chars_static = [player1, player2, player3, player4]  # lista para asociar con joysticks

    # bloques
    blocks = CustomGroup()
    border_width = 30
    border_color = (60, 30, 0)

    blocks.add(Block(border_width, screen_height, 0, 0, color=border_color))
    blocks.add(Block(screen_width, border_width, 0, 0, color=border_color))
    blocks.add(Block(border_width, screen_height, screen_width - border_width, 0, color=border_color))
    blocks.add(Block(screen_width, border_width, 0, screen_height - border_width, color=border_color))

    # plataformas
    platform_height = 5
    platform_width = 200
    platform_color = (100, 10, 100)
    height_part = (screen_height - 2 * border_width) / 4
    width_part = (screen_width - 2 * border_width) / 4

    plat1 = Platform(platform_width, platform_height,
                     width_part * 2 + border_width - platform_width / 2, height_part * 2 + border_width,
                     color=platform_color)
    plat2 = Platform(platform_width, platform_height,
                     width_part + border_width - platform_width / 2, height_part * 3 + border_width,
                     color=platform_color)
    plat3 = Platform(platform_width, platform_height,
                     width_part * 3 + border_width - platform_width / 2, height_part * 3 + border_width,
                     color=platform_color)
    plat4 = Platform(platform_width, platform_height,
                     width_part + border_width - platform_width / 2, height_part + border_width,
                     color=platform_color)
    plat5 = Platform(platform_width, platform_height,
                     width_part * 3 + border_width - platform_width / 2, height_part + border_width,
                     color=platform_color)

    # cañones
    cannon1 = Cannon(border_width, screen_height - border_width - 50, bullet_vx=6)

    cannon2 = Cannon(border_width, screen_height - border_width - 50, bullet_vx=6)
    cannon3 = Cannon(screen_width - border_width - 50,
                     height_part * 2 + border_width - 50, bullet_vx=-6)

    cannon4 = Cannon(screen_width - border_width - 50,
                     height_part * 2 + border_width - 50, bullet_vx=-6)
    cannon5 = Cannon(border_width, height_part * 3 + border_width - 50,
                     bullet_vx=8, frecuencia=40)

    cannon6 = Cannon(screen_width - border_width - 50,
                     height_part * 2 + border_width - 100, bullet_vx=-6)
    cannon7 = Cannon(border_width, border_width,
                     bullet_vx=6, bullet_vy=4)
    cannon8 = Cannon(border_width, height_part * 3 + border_width - 50,
                     bullet_vx=8, frecuencia=40)

    cannon9 = Cannon(border_width + 15, screen_height - border_width - 65,
                     bullet_vx=4, bullet_radius=30, bullet_damage=30)

    # niveles
    levels = [Level(30, [Objective((50, 100)), Objective((700, 100)), Objective((200, 500))], blocks=blocks,
                    platforms=CustomGroup(plat1, plat2, plat3, plat4, plat5),
                    cannons=CustomGroup(cannon1), fps=fps),

              Level(30, [Objective((50, 50))], blocks=blocks,
                    platforms=CustomGroup(plat2, plat3),
                    cannons=CustomGroup(cannon2, cannon3), fps=fps),

              Level(30, [Objective((350, 150))], blocks=blocks, platforms=CustomGroup(),
                    cannons=CustomGroup(cannon4, cannon5), fps=fps),

              Level(30, [Objective((150, 100)), Objective((600, 100))], blocks=blocks, platforms=CustomGroup(plat1),
                    cannons=CustomGroup(cannon6, cannon7, cannon8), fps=fps),

              Level(30, [], blocks=blocks, platforms=CustomGroup(),
                    cannons=CustomGroup(cannon9), fps=fps), ]

    level_num = 0
    level = levels[level_num]

    # controles
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    a_pressed = []
    for joystick in joysticks:
        joystick.init()
        a_pressed.append(0)
        print(joystick.get_name())

    joystick_threshold = 0.4

    play_background()
    jump_sound.set_volume(1)
    running = True
    while running:

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player1.jump()
                if event.key == pygame.K_DOWN:
                    player1.fall()

                if event.key == pygame.K_w:
                    player2.jump()
                if event.key == pygame.K_s:
                    player1.fall()

                if event.key == pygame.K_i:
                    player3.jump()
                if event.key == pygame.K_k:
                    player1.fall()

                if event.key == pygame.K_t:
                    player4.jump()
                if event.key == pygame.K_g:
                    player1.fall()

        # joysticks
        for i in range(len(joysticks)):
            if i < len(chars_static):
                if joysticks[i].get_axis(0) > joystick_threshold:
                    chars_static[i].move(5, 0)
                if joysticks[i].get_axis(0) < -joystick_threshold:
                    chars_static[i].move(-5, 0)

                if joysticks[i].get_button(0):
                    if not a_pressed[i]:
                        chars_static[i].jump()
                    a_pressed[i] = 1
                else:
                    a_pressed[i] = 0

        # teclas apretadas
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            player1.move_left()
        if pressed[pygame.K_RIGHT]:
            player1.move_right()

        if pressed[pygame.K_a]:
            player2.move_left()
        if pressed[pygame.K_d]:
            player2.move_right()

        if pressed[pygame.K_j]:
            player3.move_left()
        if pressed[pygame.K_l]:
            player3.move_right()

        if pressed[pygame.K_f]:
            player4.move_left()
        if pressed[pygame.K_h]:
            player4.move_right()

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
    subtitulo = Text("Presiona espacio o A para empezar de nuevo", screen_width / 2, screen_height / 2 + 100,
                     height=30, color=(255, 255, 255), center=True)

    jump_sound.set_volume(0)

    running = True
    while running:
        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                    return

        for i in range(len(joysticks)):
            if i < len(chars_static):
                if joysticks[i].get_button(0):
                    main()
                    return

        chars.update()
        chars.detect_collisions(blocks)

        for char in chars:
            char.jump()

        # dibujar
        screen.fill((25, 115, 200))
        blocks.draw(screen)
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
