from pygame import Surface, Rect, draw
from game.world import WORLD_DIMENSION
from rendering.constants import DISPLAY_RESOLUTION, COLOR_PLAYERS, COLOR_BACKGROUND, COLOR_BACKGROUND_SECONDARY
from game.tile import Tile

TILE_SIZE = min(DISPLAY_RESOLUTION[0] / WORLD_DIMENSION[0],
                DISPLAY_RESOLUTION[1] / WORLD_DIMENSION[1])
sub_surface_size = (TILE_SIZE * WORLD_DIMENSION[0],
                    TILE_SIZE * WORLD_DIMENSION[1])
sub_surface_border = ((DISPLAY_RESOLUTION[0] - sub_surface_size[0]) / 2,
                      (DISPLAY_RESOLUTION[1] - sub_surface_size[1]) / 2)


class AbstractRenderer:
    def render(self, target: Surface, world):
        pass


class TestRenderer(AbstractRenderer):
    def render(self, target: Surface, world):
        # background
        target.fill(COLOR_BACKGROUND)

        for x in range(WORLD_DIMENSION[0]):
            for y in range(WORLD_DIMENSION[1]):

                col = COLOR_BACKGROUND

                t = world.grid[x][y]  # type: Tile
                if t.entities:
                    col = COLOR_PLAYERS[0]

                draw.rect(target, col, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                # for x in range(WORLD_DIMENSION[0]):
                #     draw.line(target, CLR["white"], (x * TILESIZE[0], 0), (x * TILESIZE[0], RESOLUTION[1]))
                #
                # for y in range(WORLD_DIMENSION[1]):
                #     draw.line(target, CLR["white"], (0, y * TILESIZE[1]), (RESOLUTION[0], y * TILESIZE[1]))


class PerfectRenderer (AbstractRenderer):
    def __init__(self):
        self.main_surface = Surface(DISPLAY_RESOLUTION)
        self.sub_surface = self.main_surface.subsurface(Rect(sub_surface_border, sub_surface_size))

    def render(self, target: Surface, world):
        self.main_surface.fill(COLOR_BACKGROUND_SECONDARY)
        self.sub_surface.fill(COLOR_BACKGROUND)
        target.blit(self.main_surface, (0, 0))
