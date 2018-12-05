import os

import pygame

from modulos.Blocks import Block, Platform
from modulos.Characters import GravityChar, CustomGroup
from modulos.Level import Level, Objective
from modulos.Text import Text
from modulos.Weapons import Cannon

# centrar ventana
os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("tutorial FrenCoins")
    # TODO: reescalar imagen para evitar problemas con trasparencia
    pygame.display.set_icon(pygame.transform.smoothscale(pygame.image.load('static/img/FrenCoin.png'), (32, 32)))

    # personajes
    char_size = 40

    player1 = GravityChar(char_size, char_size, 600, 200, img='static/img/Tomimi.png', jumpspeed=18)
    player2 = GravityChar(char_size, char_size, 100, 350, img='static/img/LittleFrank.png', jumpspeed=18)
    player3 = GravityChar(char_size, char_size, 300, 200, img='static/img/Peiblv3.png', jumpspeed=18)
    player4 = GravityChar(char_size, char_size, 500, 100, img='static/img/Tito.png', jumpspeed=18)

    chars = CustomGroup([player1, player2, player3])
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
    cannon5 = Cannon(border_width, border_width,
                     bullet_vx=6, bullet_vy=4)

    cannon6 = Cannon(screen_width - border_width - 50,
                     height_part * 2 + border_width - 50, bullet_vx=-6)
    cannon7 = Cannon(border_width, border_width,
                     bullet_vx=6, bullet_vy=4)
    cannon8 = Cannon(screen_width - border_width - 50,
                     screen_height - border_width - 50,
                     bullet_vx=-6, bullet_vy=-2)

    # niveles
    levels = [Level(30, [Objective((50, 100)), Objective((700, 100)), Objective((200, 500))],
                    blocks=blocks, platforms=CustomGroup(plat1, plat2, plat3, plat4, plat5),
                    cannons=CustomGroup(cannon1), fps=fps),

              Level(30, [Objective((50, 100))], blocks=blocks, cannons=CustomGroup(cannon2, cannon3),
                    platforms=CustomGroup(plat2, plat3), fps=fps),

              Level(15, [Objective((350, 300))], blocks=blocks, cannons=CustomGroup(cannon4, cannon5),
                    platforms=CustomGroup(), fps=fps),

              Level(30, [Objective((150, 100)), Objective((600, 100))], blocks=blocks,
                    cannons=CustomGroup(cannon6, cannon7, cannon8),
                    platforms=CustomGroup(plat1), fps=fps), ]

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

    running = True
    while running:

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player1.jump()
                if event.key == pygame.K_w:
                    player2.jump()
                if event.key == pygame.K_i:
                    player3.jump()

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
            player1.move(dx=-5)
        if pressed[pygame.K_RIGHT]:
            player1.move(dx=5)

        if pressed[pygame.K_a]:
            player2.move(dx=-5)
        if pressed[pygame.K_d]:
            player2.move(dx=5)

        if pressed[pygame.K_j]:
            player3.move(dx=-5)
        if pressed[pygame.K_l]:
            player3.move(dx=5)

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
                level.bullets.empty()

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
    titulo = Text("Game Over", screen_width / 2, screen_height / 2,
                  height=100, color=(20, 0, 0), center=True)
    subtitulo = Text("Presiona espacio para empezar de nuevo", screen_width / 2, screen_height / 2 + 100,
                     height=30, color=(255, 255, 255), center=True)

    running = True
    while running:
        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                    break

        chars.update()
        chars.detect_collisions(blocks)

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
