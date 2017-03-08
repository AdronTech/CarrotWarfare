from rendering.ultimate_version.renderer import *


class UILayer:
    def __init__(self, renderer: UltimateRenderer, player_ui_surfaces: list[Surface]):
        self.parent_renderer = renderer
        self.player_ui_surfaces = player_ui_surfaces

    def render(self, world: World):
        pass