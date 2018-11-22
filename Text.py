import pygame

font = {}


def gen_text(text, color=(0, 0, 0), antialias=True, height=30):
    global font
    if height not in font:
        font[height] = pygame.font.Font(None, height)

    return font[height].render(text, antialias, color)
