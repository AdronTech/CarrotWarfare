from pygame import Surface, draw, Rect
from pygame.gfxdraw import aacircle, aatrigon, filled_circle, filled_trigon
from rendering.constants import *
from game.tile import Tile
from game.entity import Entity
from game.world import World
from game.carrot import Carrot
from game.player import Player
from rendering.loader import load_all


class AbstractRenderer:
    def render(self, target: Surface, world):
        pass


class PerfectRenderer(AbstractRenderer):
    def __init__(self):
        load_all()
        self.main_surface = Surface(MAIN_SURFACE_SIZE)

        print("Hello")

        # draw 4 zones
        self.main_surface.fill(COLOR_PLAYERS[0], Rect((0, 0),
                                                      (MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2)))
        self.main_surface.fill(COLOR_PLAYERS[1], Rect((MAIN_SURFACE_SIZE[0] / 2, 0),
                                                      (MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2)))
        self.main_surface.fill(COLOR_PLAYERS[2], Rect((0, MAIN_SURFACE_SIZE[1] / 2),
                                                      (MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2)))
        self.main_surface.fill(COLOR_PLAYERS[3], Rect((MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2),
                                                      (MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2)))

        self.sub_surface = self.main_surface.subsurface(Rect(SUB_SURFACE_POSITION,
                                                             SUB_SURFACE_SIZE))
        self.ground_surface = Surface(SUB_SURFACE_SIZE)
        self.ground_surface.fill(COLOR_BACKGROUND)

        self.screen_shake_current = (0, 0)

    def paint_square(self, square: (int, int), player: int):
        self.sub_surface.fill(COLOR_PLAYERS[player], Rect((square[0] * TILE_SIZE, square[1] * TILE_SIZE),
                                                          (TILE_SIZE, TILE_SIZE)))

    def render_player(self, player: Player):
        resources = IMAGE_RESOURCE["entities"]["player" + str(player.alliance)]
        image = resources["resource"]
        self.sub_surface.blit(image,
                              (int(player.pos.x *
                                   TILE_SIZE + resources["offset"][0]),
                               int(player.pos.y *
                                   TILE_SIZE + resources["offset"][1])))
        # filled_circle(self.sub_surface, int(player.pos.x * TILE_SIZE), int(player.pos.y * TILE_SIZE),
        #               int(TILE_SIZE / 2), COLOR_PLAYERS[player.alliance])
        # aacircle(self.sub_surface, int(player.pos.x * TILE_SIZE), int(player.pos.y * TILE_SIZE),
        #          int(TILE_SIZE / 2), COLOR_PLAYERS[player.alliance])

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
        self.sub_surface.blit(self.ground_surface, (0, 0))

        for y in range(WORLD_DIMENSION["height"]):

            def extract_from_tile(tile: Tile, tx, ty):
                for entity in tile.entities:
                    yield entity
                if "environment" in tile.render_flags:
                    for env_object in tile.render_flags["environment"]:
                        yield env_object, tx, ty

            row = [e for x in range(WORLD_DIMENSION["width"])
                   for e in extract_from_tile(world.grid[x][y], x, y)]  # type: list[Entity]

            def depth_sort(e):
                if issubclass(type(e), Entity):
                    return e.pos.y
                else:
                    return e[2] + 0.5

            row = sorted(row, key=depth_sort)
            for entity in row:
                e_type = type(entity)
                if e_type is Player:
                    self.render_player(entity)
                elif e_type is Carrot:
                    self.render_carrot(entity)
                # else:
                #     surf, x, y = entity
                #     self.sub_surface.blit(surf, (int(x * TILE_SIZE - surf.get_width() / 2),
                #                                  int((y + 0.5) * TILE_SIZE - surf.get_height())))

        x = SCREEN_SHAKE_OFFSET[0] * (1 + self.screen_shake_current[0])
        y = SCREEN_SHAKE_OFFSET[1] * (1 + self.screen_shake_current[1])
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
        DEFAULT_RENDERER.screen_shake_current = (random() * 2 - 1, random() * 2 - 1)
        DEFAULT_RENDERER.render(screen.render_target, game_world)

        # draw
        screen.flip()
        clock.tick(updates_per_sec)
