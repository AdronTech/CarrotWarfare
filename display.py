from pygame import display
RESOLUTION = 10, 10


class PyGameWindow:
    def __init__(self):
        self.render_target = display.set_mode(RESOLUTION)

    @staticmethod
    def flip():
        display.flip()
