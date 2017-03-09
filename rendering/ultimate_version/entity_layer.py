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
                elif e_type is Bullet:
                    pass
                else:
                    surf, x, y = entity
                    self.arena_subsurface.blit(surf, (int(x * TILE_SIZE - surf.get_width() / 2),
                                                      int((y + 0.5) * TILE_SIZE - surf.get_height())))

    def render_player(self, player: Player):
        # TODO handle player events

        resources = IMAGE_RESOURCE["entities"]
        if player.dir.x < 0:
            image = resources["player" + str(player.alliance)]["state_stand"]["left"]["frame0"]
        else:
            image = resources["player" + str(player.alliance)]["state_stand"]["right"]["frame0"]

        self.arena_subsurface.blit(image,
                                   (int(player.pos.x *
                                        TILE_SIZE + resources["player_generic"]["offset"][0]),
                                    int(player.pos.y *
                                        TILE_SIZE + resources["player_generic"]["offset"][1])))

    def render_carrot(self, carrot: Carrot):
        # TODO handle carrot events

        resources = IMAGE_RESOURCE["entities"]
        if carrot.dir.x < 0:
            image = resources["carrot" + str(carrot.alliance)]["state_stand"]["left"]["frame0"]
        else:
            image = resources["carrot" + str(carrot.alliance)]["state_stand"]["right"]["frame0"]

        self.arena_subsurface.blit(image,
                                   (int(carrot.pos.x *
                                        TILE_SIZE + resources["carrot_generic"]["offset"][0]),
                                    int(carrot.pos.y *
                                        TILE_SIZE + resources["carrot_generic"]["offset"][1])))
