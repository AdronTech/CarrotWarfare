from pygame import display
from rendering.constants import DISPLAY_RESOLUTION


class PyGameWindow:
    def __init__(self):
        self.render_target = display.set_mode(DISPLAY_RESOLUTION)

    @staticmethod
    def flip():
        display.flip()
