from rendering.ultimate_version.renderer import *


class GroundLayer:
    def __init__(self, renderer: UltimateRenderer, arena_subsurface: Surface):
        self.parent_renderer = renderer  # type: UltimateRenderer
        self.ground_surface = Surface(SUB_SURFACE_SIZE)
        self.ground_surface.fill(COLOR_BACKGROUND)
        self.arena_subsurface = arena_subsurface

    def render(self, world: World):
        self.arena_subsurface.blit(self.ground_surface, (0, 0))
