from settings.GUI import SCREEN_HEIGHT, SCREEN_WIDTH, CANNON_SIZE, COIN_SIZE
from settings.Game import CHAR_SPEED

block_width = 30
platform_width = 200
platform_height = 6

height_fourth = (SCREEN_HEIGHT - 2 * block_width) / 4
floor3 = height_fourth + block_width
floor2 = height_fourth * 2 + block_width
floor1 = height_fourth * 3 + block_width

width_fourth = (SCREEN_WIDTH - 2 * block_width) / 4
col1 = width_fourth + block_width
col2 = width_fourth * 2 + block_width
col3 = width_fourth * 3 + block_width

level1 = {
    "duration": 30,

    "blocks": [
        {
            "width": block_width, "height": SCREEN_HEIGHT, "x": 0, "y": 0
        }, {
            "width": SCREEN_WIDTH, "height": block_width, "x": 0, "y": 0
        }, {
            "width": block_width, "height": SCREEN_HEIGHT, "x": SCREEN_WIDTH - block_width, "y": 0
        }, {
            "width": SCREEN_WIDTH, "height": block_width, "x": 0, "y": SCREEN_HEIGHT - block_width
        },
    ],

    "platforms": [
        {
            "width": platform_width, "height": platform_height, "x": col2 - platform_width / 2, "y": floor2
        }, {
            "width": platform_width, "height": platform_height, "x": col1 - platform_width / 2, "y": floor1
        }, {
            "width": platform_width, "height": platform_height, "x": col3 - platform_width / 2, "y": floor1
        }, {
            "width": platform_width, "height": platform_height, "x": col1 - platform_width / 2, "y": floor3
        }, {
            "width": platform_width, "height": platform_height, "x": col3 - platform_width / 2, "y": floor3
        },
    ],

    "cannons": [
        {
            "x": block_width, "y": SCREEN_HEIGHT - block_width - CANNON_SIZE, "x_speed": CHAR_SPEED + 1
        },
    ],

    "coins": [
        {
            "x": block_width + 20, "y": block_width + 20
        }, {
            "x": SCREEN_WIDTH - block_width - COIN_SIZE - 20, "y": block_width + 20
        }, {
            "x": col1 - COIN_SIZE / 2, "y": SCREEN_HEIGHT - block_width - COIN_SIZE - 20
        },
    ]
}
