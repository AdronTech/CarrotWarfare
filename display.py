from pygame import display
from pygame.locals import *


class PyGameWindow:
    def __init__(self):
        self.fullscreen = False
        from rendering.constants import RENDER_RESOLUTION
        self.window_resolution = RENDER_RESOLUTION
        self.render_target = None
        self.reset_mode()

    def reset_mode(self):
        if self.fullscreen:
            self.render_target = display.set_mode(self.window_resolution, FULLSCREEN)
        else:
            self.render_target = display.set_mode(self.window_resolution)

    @staticmethod
    def flip():
        display.flip()
