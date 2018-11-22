import pygame
import random

from Blocks import Block, Platform
from Characters import GravityChar, CustomGroup, Kirby
from Weapons import Bullet
from Level import Level, Objective
from Text import gen_text


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("tutorial pygame")

    # personajes
    char_size = 40

    player1 = GravityChar(char_size, char_size, 600, 200, img='img/Pina.png', jumpspeed=18)
    player2 = Kirby(char_size, char_size, 100, 200, img='img/diggo.png', jumpspeed=8)
    player3 = GravityChar(char_size, char_size, 300, 200, img='img/LittleFrank.png', jumpspeed=18)

    chars = CustomGroup([player1, player2, player3])

    # proyectile
    bullets = CustomGroup()

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

    # objetivos
    objective1 = Objective((50, 100))
    objective2 = Objective((700, 100))
    objective3 = Objective((200, 500))

    # niveles
    levels = [Level(30, [objective1, objective2, objective3], fps=fps),
              Level(15, [objective1], fps=fps),
              Level(15, [Objective((350, 300))], fps=fps),
              Level(15, [Objective((150, 100)), Objective((600, 100))], fps=fps), ]

    level_platforms = [CustomGroup(plat1, plat2, plat3, plat4, plat5),
                       CustomGroup(plat2, plat3),
                       CustomGroup(plat4, plat5),
                       CustomGroup(plat1), ]

    level_num = 0
    level = levels[level_num]
    platforms = level_platforms[level_num]

    # controles
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()

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

                if event.key == pygame.K_r:
                    player3.jump()

        for joystick in joysticks:
            print(joystick.get_axis(0), joystick.get_axis(1))

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

        if pressed[pygame.K_SPACE]:
            b = Bullet(5,
                       random.randint(int(screen_width / 3), int(screen_width / 3 * 2)),
                       random.randint(int(screen_height / 3), int(screen_height / 3 * 2)),
                       random.randint(-1, 1) * 6, random.randint(-1, 1) * 6,
                       color=(50, 50, 50))
            if b.vx == 0 and b.vy == 0:
                b.vx = -1 ^ random.randint(1, 2) * 6
            bullets.add(b)

        # mov automático
        chars.update()
        bullets.update()
        level.update()

        # colisiones
        chars.detect_collisions(blocks)
        chars.detect_collisions(platforms)
        for _ in chars:
            chars.detect_collisions(chars)

        blocks.detect_impacts(bullets)
        chars.detect_impacts(bullets)
        chars.detect_objectives(level.objectives)

        # terminar ronda
        if level.is_over():
            level.end(chars)
            level_num += 1

            if level_num >= len(levels):
                running = False
            else:
                level = levels[level_num]
                platforms = level_platforms[level_num]

        if len(chars) == 0:
            running = False

        # dibujar
        screen.fill((25, 115, 200))
        blocks.draw(screen)
        platforms.draw(screen)
        level.draw(screen)
        chars.draw(screen)
        bullets.draw(screen)

        # actualizar y esperar un tick
        pygame.display.flip()
        clock.tick(fps)

    # pantalla final
    titulo = gen_text("Game Over", height=100, color=(20, 0, 0))
    subtitulo = gen_text("Presiona espacio para empezar de nuevo", height=30, color=(255, 255, 255))
    pos = titulo.get_rect()
    pos.center = (screen_width / 2, screen_height / 2)

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
        screen.blit(titulo, pos)
        screen.blit(subtitulo, pos.move(0, 100))

        # actualizar y esperar un tick
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    return


if __name__ == "__main__":
    main()
