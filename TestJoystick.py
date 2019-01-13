import os

import pygame
from pygame.locals import *

from modulos.elements.Text import Text

os.environ['SDL_VIDEO_CENTERED'] = '1'


def test_joystick():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60

    screen = pygame.display.set_mode((800, 600))

    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()
        print(joystick.get_name())

    joy_id = 0
    running = True

    while running:

        # eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                if event.key == K_SPACE:
                    joy_id += 1
                    joy_id %= pygame.joystick.get_count()

        # joystick
        joystick = joysticks[joy_id]
        titulo = f'Testeando joystick {joy_id}: {joystick.get_name()}'
        intruccion = 'presiona espacio para cambiar de joystick'

        ejes = ""
        for i in range(joystick.get_numaxes()):
            ejes += f'{i} : {round(joystick.get_axis(i), 1)}  |  '
        ejes = ejes[:-5]

        botones = ""
        apretados = 0
        for i in range(joystick.get_numbuttons()):
            if joystick.get_button(i):
                botones += f'{i} '
                apretados += 1

        if apretados == 1:
            botones = f'boton {botones}apretado'
        elif apretados > 1:
            botones = f'botones {botones}apretados'
        else:
            botones = "no hay botones apretados"

        hats = ""
        for i in range(joystick.get_numhats()):
            hats += f'{i} : {joystick.get_hat(i)}  |  '
        hats = hats[:-5]

        screen.fill((200, 200, 200))
        Text(titulo, 400, 100, center=True, height=20).draw(screen)
        Text(intruccion, 400, 130, center=True, height=20).draw(screen)

        Text("Ejes", 400, 200, center=True, height=30).draw(screen)
        Text(ejes, 400, 235, center=True, height=30).draw(screen)
        Text(botones, 400, 318, center=True, height=20).draw(screen)
        Text("Hats", 400, 400, center=True, height=30).draw(screen)
        Text(hats, 400, 435, center=True, height=30).draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    return


if __name__ == "__main__":
    test_joystick()
