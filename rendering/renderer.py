from pygame import Surface, Rect, draw
from game.world import WORLD_DIMENSION
from display import RESOLUTION
from game.tile import Tile

TILESIZE = (RESOLUTION[0] / WORLD_DIMENSION[0],
            RESOLUTION[1] / WORLD_DIMENSION[1])

CLR = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0)
}


class AbstractRenderer :
    def render(self, target, world):
        pass


class TestRenderer (AbstractRenderer):

    def render(self, target: Surface, world):
        # background
        target.fill(CLR["black"])

        for x in range(WORLD_DIMENSION[0]):
            for y in range(WORLD_DIMENSION[1]):

                col = CLR["white"]

                t = world.grid[x][y]  # type: Tile
                if t.entities:
                    col = CLR["red"]

                draw.rect(target, col, Rect((x*TILESIZE[0], y*TILESIZE[1]), TILESIZE))

        # for x in range(WORLD_DIMENSION[0]):
        #     draw.line(target, CLR["white"], (x * TILESIZE[0], 0), (x * TILESIZE[0], RESOLUTION[1]))
        #
        # for y in range(WORLD_DIMENSION[1]):
        #     draw.line(target, CLR["white"], (0, y * TILESIZE[1]), (RESOLUTION[0], y * TILESIZE[1]))