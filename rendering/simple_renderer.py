from game.tile import TileState
from rendering.abstract_renderer import *
from pygame import Surface, Rect, draw
from cmath import pi

CLR = {"white": (255, 255, 255), "black": (0, 0, 0)}


class SimpleRenderer(AbstractRenderer):
    def render_player(self, target, player: Player):
        angle = -player.dir.as_polar()[1]
        draw.arc(target,
                 COLOR_PLAYERS[player.alliance],
                 Rect(int((player.pos.x - player.attack_range) * TILE_SIZE),
                      int((player.pos.y - player.attack_range) * TILE_SIZE),
                      int(player.attack_range * TILE_SIZE * 2),
                      int(player.attack_range * TILE_SIZE * 2)),
                 (angle - player.attack_angle/2)*pi/180,
                 (angle + player.attack_angle/2)*pi/180,
                 5)

        # print(angle)

        draw.circle(target, COLOR_PLAYERS[player.alliance],
                    (int(player.pos.x * TILE_SIZE), int(player.pos.y * TILE_SIZE)),
                    int(TILE_SIZE / 2))

    def render_carrot(self, target, carrot: Carrot):

        angle = -carrot.dir.as_polar()[1]
        draw.arc(target,
                 COLOR_PLAYERS[carrot.alliance],
                 Rect(int((carrot.pos.x - carrot.attack_range) * TILE_SIZE),
                      int((carrot.pos.y - carrot.attack_range) * TILE_SIZE),
                      int(carrot.attack_range * TILE_SIZE * 2),
                      int(carrot.attack_range * TILE_SIZE * 2)),
                 (angle - carrot.attack_angle / 2) * pi / 180,
                 (angle + carrot.attack_angle / 2) * pi / 180,
                 5)

        draw.polygon(target, COLOR_PLAYERS[carrot.alliance],
                     [(int(carrot.pos.x * TILE_SIZE), int(carrot.pos.y * TILE_SIZE)),
                      (int((carrot.pos.x + 0.3) * TILE_SIZE),
                       int((carrot.pos.y - 1) * TILE_SIZE)),
                      (int((carrot.pos.x - 0.3) * TILE_SIZE),
                       int((carrot.pos.y - 1) * TILE_SIZE))])

    def render(self, target: Surface, world: World):
        target.fill(CLR["white"])
        for x in range(WORLD_DIMENSION["width"]):
            for y in range(WORLD_DIMENSION["height"]):
                t = world.grid[x][y]
                if t.state and t.state["name"] == TileState.growing:
                    size = t.state["g_state"] / 4 * TILE_SIZE
                    draw.rect(target, COLOR_PLAYERS[t.state["alliance"]],
                              Rect((int(x * TILE_SIZE + (TILE_SIZE - size) / 2),
                                    int(y * TILE_SIZE + (TILE_SIZE - size) / 2)),
                                   (size, size)))

        for e in world.entities:
            if type(e) is Player:
                self.render_player(target, e)
            elif type(e) is Carrot:
                self.render_carrot(target, e)
