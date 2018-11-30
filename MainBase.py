import os

import pygame

from Blocks import Block, Platform
from CharactersBase import GravityChar, CustomGroup
from Text import Text

# centrar ventana
os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("tutorial pygame")

    # personajes
    char_size = 50

    # GravityChar(ancho, alto, pos_x, pos_y)
    player1 = GravityChar(char_size, char_size, 600, 200, img='img/Pina.png', jumpspeed=18)
    player2 = GravityChar(char_size, char_size, 300, 200, img='img/Tomimi.png', jumpspeed=18)

    chars = CustomGroup([player1, player2])

    # bloques
    blocks = CustomGroup()
    border_width = 30
    border_color = (40, 20, 0)

    # Block(ancho, alto, pos_x, pos_y, color)
    blocks.add(Block(border_width, screen_height, 0, 0, color=border_color))
    blocks.add(Block(screen_width, border_width, 0, 0, color=border_color))
    blocks.add(Block(border_width, screen_height, screen_width - border_width, 0, color=border_color))
    blocks.add(Block(screen_width, border_width, 0, screen_height - border_width, color=border_color))

    # plataformas
    platform_height = 5
    platform_width = 200
    platform_color = (100, 50, 0)

    # 1/4 del ancho y del alto
    height_part = (screen_height - 2 * border_width) / 4
    width_part = (screen_width - 2 * border_width) / 4

    # Platform(ancho, alto, pos_x, pos_y)
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

    platforms = CustomGroup(plat1, plat2, plat3, plat4, plat5)

    indicacion = Text("Jugador 1 usa flechas para moverse, jugador 2 usa zsc... wat?",
                      screen_width / 2, 17, center=True, color=(200, 200, 200))
    indicacion2 = Text("(de esta manera no se bloquea el input en mi teclado)",
                       screen_width / 2, 37, center=True, color=(200, 200, 200), height=20)

    running = True
    while running:

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player1.jump()
                if event.key == pygame.K_s:
                    player2.jump()

        # teclas apretadas
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            player1.move(dx=-5)
        if pressed[pygame.K_RIGHT]:
            player1.move(dx=5)

        if pressed[pygame.K_z]:
            player2.move(dx=-5)
        if pressed[pygame.K_c]:
            player2.move(dx=5)

        # mov automático
        chars.update()

        # colisiones
        chars.detect_collisions(blocks)
        chars.detect_collisions(platforms)

        # para asegurarse de que no hayan problemas con las colisiones entre objetos que se mueven,
        # hay que detectar las colisiones n veces (debido a que al resolver una colisión pueden
        # aparecer nuevas colisiones en cadena)
        for _ in chars:
            chars.detect_collisions(chars)

        # dibujar
        screen.fill((25, 115, 200))  # rellenar fondo
        blocks.draw(screen)
        platforms.draw(screen)
        indicacion.draw(screen)
        indicacion2.draw(screen)
        chars.draw(screen)

        # actualizar y esperar un tick
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    return


if __name__ == "__main__":
    main()
