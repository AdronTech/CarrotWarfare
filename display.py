from pygame import display
from pygame.locals import *
from rendering.constants import RENDER_RESOLUTION


class PyGameWindow:
    def __init__(self):
        self.full_screen = True
        self.render_target = None
        self.reset_mode()

    def reset_mode(self):
        if self.full_screen:
            self.render_target = display.set_mode(RENDER_RESOLUTION, FULLSCREEN)
        else:
            self.render_target = display.set_mode(RENDER_RESOLUTION)

    @staticmethod
    def flip():
        display.flip()
