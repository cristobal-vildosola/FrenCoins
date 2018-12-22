import json

from modulos.Blocks import Block, Platform
from modulos.Characters import CustomGroup
from modulos.Level import Level, Coin
from modulos.Weapons import Cannon


def load_level(level_json):
    with open(level_json) as f:
        level = json.load(f)

    blocks = CustomGroup()
    for block in level["blocks"]:
        blocks.add(Block(**block))

    platforms = CustomGroup()
    for platform in level["platforms"]:
        platforms.add(Platform(**platform))

    cannons = CustomGroup()
    for cannon in level["cannons"]:
        cannons.add(Cannon(**cannon))

    coins = CustomGroup()
    for coin in level["coins"]:
        coins.add(Coin(**coin))

    return Level(duration=level["duration"], coins=coins, cannons=cannons, blocks=blocks, platforms=platforms)
