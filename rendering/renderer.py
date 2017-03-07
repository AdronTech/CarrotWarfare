from pygame import Surface, draw
from pygame.gfxdraw import aacircle, aatrigon, filled_circle, filled_trigon
from rendering.constants import *
from game.tile import Tile
from game.world import World
from game.carrot import Carrot
from game.player import Player


class AbstractRenderer:
    def render(self, target: Surface, world):
        pass


class TestRenderer(AbstractRenderer):
    def render(self, target: Surface, world: World):
        # background
        target.fill(COLOR_BACKGROUND)

        for x in range(WORLD_DIMENSION["width"]):
            for y in range(WORLD_DIMENSION["height"]):

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
        self.screen_shake_current = (0, 0)

    def paint_square(self, square: (int, int), player: int):
        self.sub_surface.fill(COLOR_PLAYERS[player], Rect((square[0] * TILE_SIZE, square[1] * TILE_SIZE),
                                                          (TILE_SIZE, TILE_SIZE)))

    def render_player(self, player: Player):
        # self.sub_surface.blit(IMAGE_RESOURCE["entities"]["player"+player.alliance]["resource"])
        filled_circle(self.sub_surface, int(player.pos.x * TILE_SIZE), int(player.pos.y * TILE_SIZE),
                      int(TILE_SIZE / 2), COLOR_PLAYERS[player.alliance])
        aacircle(self.sub_surface, int(player.pos.x * TILE_SIZE), int(player.pos.y * TILE_SIZE),
                 int(TILE_SIZE / 2), COLOR_PLAYERS[player.alliance])

    def render_carrot(self, carrot: Carrot):
        filled_trigon(self.sub_surface,
                      int(carrot.pos.x * TILE_SIZE),
                      int(carrot.pos.y * TILE_SIZE),
                      int((carrot.pos.x + 0.3) * TILE_SIZE),
                      int((carrot.pos.y - 1) * TILE_SIZE),
                      int((carrot.pos.x - 0.3) * TILE_SIZE),
                      int((carrot.pos.y - 1) * TILE_SIZE),
                      COLOR_PLAYERS[carrot.alliance])
        aatrigon(self.sub_surface,
                 int(carrot.pos.x * TILE_SIZE),
                 int(carrot.pos.y * TILE_SIZE),
                 int((carrot.pos.x + 0.3) * TILE_SIZE),
                 int((carrot.pos.y - 1) * TILE_SIZE),
                 int((carrot.pos.x - 0.3) * TILE_SIZE),
                 int((carrot.pos.y - 1) * TILE_SIZE),
                 COLOR_PLAYERS[carrot.alliance])

    # def render_plant_melee(self, plant: PlantMelee):
    #     pass

    # def render_plant_ranged(self, plant: PlantRanged):
    #     pass

    def render(self, target: Surface, world: World):
        self.sub_surface.fill(COLOR_BACKGROUND)
        x = SCREEN_SHAKE_OFFSET[0] * (1 + self.screen_shake_current[0])
        y = SCREEN_SHAKE_OFFSET[1] * (1 + self.screen_shake_current[1])
        for i in range(len(world.entities)):
            entity = world.entities[i]
            e_type = type(entity)
            if e_type is Player:
                self.render_player(entity)
            if e_type is Carrot:
                self.render_carrot(entity)

        target.blit(self.main_surface, (0, 0), Rect((x, y), DISPLAY_RESOLUTION))


if __name__ == "__main__":
    from pygame import init as pygame_init
    from pygame import event as pygame_events
    from pygame.time import Clock
    from timing import redraw_counter, updates_per_sec
    from display import PyGameWindow
    from pygame.display import set_mode
    from pygame.locals import *
    from random import randint, random

    pygame_init()
    screen = PyGameWindow()
    set_mode(DISPLAY_RESOLUTION, RESIZABLE)

    DEFAULT_RENDERER = PerfectRenderer()

    game_world = World()

    # main loop
    clock = Clock()
    while True:
        # event
        for e in pygame_events.get():
            if e.type is QUIT:
                quit()
            if e.type is VIDEORESIZE:
                DISPLAY_RESOLUTION = e.size

        print(DISPLAY_RESOLUTION)

        pygame_events.pump()
        # update
        game_world.update()
        # render
        next(redraw_counter)

        DEFAULT_RENDERER.paint_square((randint(0, 19), randint(0, 19)), randint(0, 3))
        # DEFAULT_RENDERER.screen_shake_current = (random() * 2 - 1, random() * 2 - 1)
        DEFAULT_RENDERER.render(screen.render_target, game_world)

        # draw
        screen.flip()
        clock.tick(updates_per_sec)
