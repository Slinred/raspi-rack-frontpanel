import os


class Constants:
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    )

    RES_DIR = os.path.join(BASE_DIR, "res")

    SCREEN_WIDTH = 128
    SCREEN_HEIGHT = 32
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    SCREEN_REDRAW_INTERVAL = 1

    I2C_BUS_ID = 1
    DISPLAY_I2C_ADDRESS = 0x3C

    DEFAULT_FONT = "DejaVuSans.ttf"
    DEFAULT_HSPACE = 1
    DEFAULT_VSPACE = 1
    SCREEN_TEXT_CONFIG = {
        1: {"FONT_SIZE": 14, "HSPACE": (SCREEN_HEIGHT - 14) / 2, "VSPACE": 0},
        2: {"FONT_SIZE": 10, "HSPACE": 3, "VSPACE": 2},
        3: {"FONT_SIZE": 8, "HSPACE": 2, "VSPACE": 2},
        4: {"FONT_SIZE": 5, "HSPACE": 2, "VSPACE": 2},
    }
