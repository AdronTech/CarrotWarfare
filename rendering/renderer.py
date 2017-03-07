from pygame import Surface, Rect, draw
from rendering.constants import *
from game.tile import Tile


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


class PerfectRenderer(AbstractRenderer):
    def __init__(self):
        self.main_surface = Surface(DISPLAY_RESOLUTION)
        self.sub_surface = self.main_surface.subsurface(Rect(SUB_SURFACE_BORDER, SUB_SURFACE_SIZE))

    def paint_square(self, square: (int, int), player: int):
        self.sub_surface.fill(COLOR_PLAYERS[player], Rect((square[0] * TILE_SIZE, square[1] * TILE_SIZE),
                                                          (TILE_SIZE, TILE_SIZE)))

    def render(self, target: Surface, world):
        self.main_surface.fill(COLOR_BACKGROUND_SECONDARY)
        self.sub_surface.fill(COLOR_BACKGROUND)
        self.paint_square((0, 0), 0)
        self.paint_square((0, 1), 3)
        self.paint_square((1, 0), 3)
        self.paint_square((19, 19), 2)
        target.blit(self.main_surface, (0, 0))


if __name__ == "__main__":
    pass
