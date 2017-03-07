from pygame import Surface, Rect, draw
from rendering.constants import *
from game.tile import Tile
from game.world import World


class AbstractRenderer:
    def render(self, target: Surface, world):
        pass


class TestRenderer(AbstractRenderer):
    def render(self, target: Surface, world: World):
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
        self.main_surface = Surface(MAIN_SURFACE_SIZE)
        self.sub_surface = self.main_surface.subsurface(Rect(SUB_SURFACE_POSITION,
                                                             SUB_SURFACE_SIZE))
        self.main_surface.fill(COLOR_BACKGROUND_SECONDARY)
        self.sub_surface.fill(COLOR_BACKGROUND)
        self.screen_shake_current = (0, 0)

    def paint_square(self, square: (int, int), player: int):
        self.sub_surface.fill(COLOR_PLAYERS[player], Rect((square[0] * TILE_SIZE, square[1] * TILE_SIZE),
                                                          (TILE_SIZE, TILE_SIZE)))

    def render(self, target: Surface, world: World):
        x = SCREEN_SHAKE_OFFSET[0] * (1 + self.screen_shake_current[0])
        y = SCREEN_SHAKE_OFFSET[1] * (1 + self.screen_shake_current[1])
        target.blit(self.main_surface, (0, 0), Rect((x, y), DISPLAY_RESOLUTION))


if __name__ == "__main__":
    from pygame import init as pygame_init
    from pygame import event as pygame_events
    from pygame.time import Clock
    from timing import redraw_counter, updates_per_sec
    from display import PyGameWindow
    from pygame.locals import *
    from random import randint, random

    pygame_init()
    display = PyGameWindow()
    DEFAULT_RENDERER = PerfectRenderer()

    game_world = World()

    # main loop
    clock = Clock()
    while True:
        # event
        for e in pygame_events.get(QUIT):
            if e.type is QUIT:
                quit()
        pygame_events.pump()
        # update
        game_world.update()
        # render
        next(redraw_counter)
        DEFAULT_RENDERER.paint_square((randint(0, 19), randint(0, 19)), randint(0, 3))
        DEFAULT_RENDERER.screen_shake_current = (random() * 2 - 1, random() * 2 - 1)
        DEFAULT_RENDERER.render(display.render_target, game_world)
        # draw
        display.flip()
        clock.tick(updates_per_sec)
