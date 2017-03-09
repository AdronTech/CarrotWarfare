from rendering.ultimate_version.renderer import *


class EntityLayer:
    def __init__(self, renderer: UltimateRenderer, arena_subsurface: Surface):
        self.parent_renderer = renderer
        self.arena_subsurface = arena_subsurface

    def render(self, world: World):
        # for every horizontal line
        for y in range(WORLD_DIMENSION["height"]):

            # get all items in tile
            def extract_from_tile(tile: Tile, tx, ty):
                for e in tile.entities:
                    yield e
                if "environment" in tile.render_flags:
                    for env_object in tile.render_flags["environment"]:
                        yield env_object, tx, ty

            # generate rows
            row = [e for x in range(WORLD_DIMENSION["width"])
                   for e in extract_from_tile(world.grid[x][y], x, y)]  # type: list[Entity]

            # depth sort
            def depth_sort(e):
                if issubclass(type(e), Entity):
                    return e.pos.y
                else:
                    return e[2] + 0.5

            row = sorted(row, key=depth_sort)

            # draw
            for entity in row:
                e_type = type(entity)
                if e_type is Player:
                    self.render_player(entity)
                elif e_type is Carrot:
                    self.render_carrot(entity)
                elif e_type is Sprout:
                    pass
                else:
                    surf, x, y = entity
                    self.arena_subsurface.blit(surf, (int(x * TILE_SIZE - surf.get_width() / 2),
                                                      int((y + 0.5) * TILE_SIZE - surf.get_height())))

    def render_player(self, player: Player):
        # TODO handle player events
        resources = IMAGE_RESOURCE["entities"]["player" + str(player.alliance)]
        image = resources["resource"]
        self.arena_subsurface.blit(image,
                                   (int(player.pos.x *
                                        TILE_SIZE + resources["offset"][0]),
                                    int(player.pos.y *
                                        TILE_SIZE + resources["offset"][1])))

    def render_carrot(self, carrot: Carrot):
        # TODO handle carrot events
        filled_trigon(self.arena_subsurface,
                      int(carrot.pos.x * TILE_SIZE),
                      int(carrot.pos.y * TILE_SIZE),
                      int((carrot.pos.x + 0.3) * TILE_SIZE),
                      int((carrot.pos.y - 1) * TILE_SIZE),
                      int((carrot.pos.x - 0.3) * TILE_SIZE),
                      int((carrot.pos.y - 1) * TILE_SIZE),
                      COLOR_PLAYERS[carrot.alliance])
        aatrigon(self.arena_subsurface,
                 int(carrot.pos.x * TILE_SIZE),
                 int(carrot.pos.y * TILE_SIZE),
                 int((carrot.pos.x + 0.3) * TILE_SIZE),
                 int((carrot.pos.y - 1) * TILE_SIZE),
                 int((carrot.pos.x - 0.3) * TILE_SIZE),
                 int((carrot.pos.y - 1) * TILE_SIZE),
                 COLOR_PLAYERS[carrot.alliance])
