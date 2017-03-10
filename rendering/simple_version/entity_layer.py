from rendering.simple_version.renderer import *
from math import pi

class EntityLayer:
    def __init__(self, renderer: SimpleRenderer, arena_subsurface: Surface):
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
                    self.render_sprout(entity)
                elif e_type is Bullet:
                    self.render_bullet(entity)
                else:
                    surf, x, y = entity
                    self.arena_subsurface.blit(surf, (int(x * TILE_SIZE - surf.get_width() / 2),
                                                      int((y + 0.5) * TILE_SIZE - surf.get_height())))

    def render_player(self, player: Player):
        angle = -player.dir.as_polar()[1]
        draw.arc(self.arena_subsurface,
                 COLOR_PLAYERS[player.alliance],
                 Rect(int((player.pos.x - player.attack_range) * TILE_SIZE),
                      int((player.pos.y - player.attack_range) * TILE_SIZE),
                      int(player.attack_range * TILE_SIZE * 2),
                      int(player.attack_range * TILE_SIZE * 2)),
                 (angle - player.attack_angle / 2) * pi / 180,
                 (angle + player.attack_angle / 2) * pi / 180,
                 5)

        # print(angle)

        draw.circle(self.arena_subsurface, COLOR_PLAYERS[player.alliance],
                    (int(player.pos.x * TILE_SIZE), int(player.pos.y * TILE_SIZE)),
                    int(TILE_SIZE / 2))

    def render_carrot(self, carrot: Carrot):

        angle = -carrot.dir.as_polar()[1]
        draw.arc(self.arena_subsurface,
                 COLOR_PLAYERS[carrot.alliance],
                 Rect(int((carrot.pos.x - carrot.attack_range) * TILE_SIZE),
                      int((carrot.pos.y - carrot.attack_range) * TILE_SIZE),
                      int(carrot.attack_range * TILE_SIZE * 2),
                      int(carrot.attack_range * TILE_SIZE * 2)),
                 (angle - carrot.attack_angle / 2) * pi / 180,
                 (angle + carrot.attack_angle / 2) * pi / 180,
                 5)

        draw.polygon(self.arena_subsurface, COLOR_PLAYERS[carrot.alliance],
                     [(int(carrot.pos.x * TILE_SIZE), int(carrot.pos.y * TILE_SIZE)),
                      (int((carrot.pos.x + 0.3) * TILE_SIZE),
                       int((carrot.pos.y - 1) * TILE_SIZE)),
                      (int((carrot.pos.x - 0.3) * TILE_SIZE),
                       int((carrot.pos.y - 1) * TILE_SIZE))])

    def render_sprout(self, sprout: Sprout):

        angle = -sprout.dir.as_polar()[1]
        r = 1
        h = 1

        if sprout.state in [SproutState.attack, SproutState.idle]:
            h = 0.5

        draw.arc(self.arena_subsurface,
                 COLOR_PLAYERS[sprout.alliance],
                 Rect(int((sprout.pos.x - r) * TILE_SIZE),
                      int((sprout.pos.y - r) * TILE_SIZE),
                      int(r * TILE_SIZE * 2),
                      int(r * TILE_SIZE * 2)),
                 (angle - sprout.attack_angle / 2) * pi / 180,
                 (angle + sprout.attack_angle / 2) * pi / 180,
                 5)

        draw.polygon(self.arena_subsurface,
                     COLOR_PLAYERS[sprout.alliance],
                     [
                         ((sprout.pos.x - 0.4) * TILE_SIZE, sprout.pos.y * TILE_SIZE),
                         ((sprout.pos.x + 0.4) * TILE_SIZE, sprout.pos.y * TILE_SIZE),
                         ((sprout.pos.x + 0.2) * TILE_SIZE, (sprout.pos.y - h) * TILE_SIZE),
                         ((sprout.pos.x - 0.2) * TILE_SIZE, (sprout.pos.y - h) * TILE_SIZE)
                     ])
        for e in sprout.events:
            if e["name"] == "attack":
                sprout.hard_lock = IMAGE_RESOURCE["entities"]["sprout_generic"]["attack_hard_lock"]
                sprout.soft_lock = IMAGE_RESOURCE["entities"]["sprout_generic"]["attack_soft_lock"]

        sprout.events.clear()

    def render_bullet(self, bullet: Bullet):

        draw.circle(self.arena_subsurface, COLOR_PLAYERS_DARK[bullet.alliance], (int(bullet.pos.x * TILE_SIZE), int(bullet.pos.y * TILE_SIZE)), int(0.25 * TILE_SIZE))
