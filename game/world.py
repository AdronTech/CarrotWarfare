from game.tile import *
from timing import *
from random import random, randint
from rendering import debugger as Debug
from pygame import Color
from game.constants import *
from math import floor

if False:
    from game.player import Player, SeedType
    from game.carrot import Carrot
    from game.sprout import Sprout
    from game.entity import Entity
    from game.bullet import Bullet

WORLD_DIMENSION = {"width": 27, "height": 17}

SPAWN_POSITIONS = [(1, 1),
                   (WORLD_DIMENSION["width"] - 1, 1),
                   (1, WORLD_DIMENSION["height"] - 1),
                   (WORLD_DIMENSION["width"] - 1, WORLD_DIMENSION["height"] - 1)]


class World:
    def __init__(self):

        self.player_count = 0
        w = WORLD_DIMENSION["width"]
        h = WORLD_DIMENSION["height"]
        self.entities = []
        self.events = []  # type: [{}]
        self.growing = []  # type: [Tile]
        self.players = [None] * 4
        self.grid = [[Tile(self.events, x, y) for y in range(h)] for x in range(w)]  # type: [
        self.respawn_time = 2.5

    def radius_gen(self, pos, r):
        for dx in range(-r, r + 1):
            for dy in range(-(r - abs(dx)), r - abs(dx) + 1):
                yield Vector2(pos) + Vector2(dx, dy)

    def spiral_gen(self):
        r = 0
        yield Vector2(0, 0)
        while True:
            r += 1
            x, y = (0, r)
            while x < r:
                yield Vector2(x, y)
                yield Vector2(-x, -y)
                yield Vector2(y, -x)
                yield Vector2(-y, x)
                y -= 1
                x += 1

    def int_vec(self, pos):
        x, y = pos

        x = int(x)
        y = int(y)

        return Vector2(x, y)

    def get_tile(self, pos):
        x, y = pos

        x = floor(x)
        y = floor(y)

        if x < 0 or y < 0 or x >= WORLD_DIMENSION["width"] or y >= WORLD_DIMENSION["height"]:
            return None

        return self.grid[x][y]

    def update(self, commands):

        self.events.clear()

        for i in range(len(self.growing)):
            self.growing[i].update()

        for i in range(4):
            if self.players[i]:
                player = self.players[i]  # type: Player
                player.update(commands[i])

        for i in range(self.player_count, len(self.entities)):
            ent = self.entities[i]  # type: Entity
            ent.update()
        #
        # for col in self.grid:
        #     for t in col:
        #         if t.collider:
        #             Debug.circle((0, 0, 0, 255), (t.x + 0.5, t.y + 0.5), 0.2)

        self.check_events()

        # print(self.events)


    def check_events(self):
        from game.carrot import Carrot
        from game.sprout import Sprout
        from game.player import Player, SeedType
        from game.bullet import Bullet

        for e in self.events:  # type: dict
            if e["name"] == "plant_request":
                t = e["tile"]
                if not t.state:
                    if e["author"].consume_seeds(1, e["type"]):
                        self.growing.append(t)
                        t.plant(e["type"], e["alliance"])
                        e["allowed"] = None
            elif e["name"] == "full_grown":
                self.growing.remove(e["tile"])

                if e["type"] is SeedType.melee:
                    self.entities.append(Carrot(self, e["alliance"], e["pos"]))
                elif e["type"] is SeedType.ranged:
                    self.entities.append(Sprout(self, e["alliance"], e["pos"]))
            elif e["name"] == "attack":
                pos = e["pos"]  # type: Vector2
                dir = e["dir"]
                r = e["range"]
                h_angle = e["angle"] / 2

                possible_enemies = []  # type: [Entity]

                for x in range(int(e["pos"].x - r), int(e["pos"].x + r + 1)):
                    for y in range(int(e["pos"].y - r), int(e["pos"].y + r + 1)):
                        t = self.get_tile((x, y))
                        if not t:
                            continue

                        for ent in t.entities:  # type: Entity
                            if e["alliance"] != ent.alliance:
                                dist = ent.pos - pos  # type: Vector2

                                if dist.length_squared() > r ** 2:
                                    continue

                                if abs(dist.angle_to(dir)) > h_angle:
                                    continue

                                possible_enemies.append((dist.length_squared(), ent))

                possible_enemies = sorted(possible_enemies, key=lambda entity: entity[0])  # sort by distance
                for i in range(min(e["count"], len(possible_enemies))):
                    possible_enemies[i][1].hit(e["damage"])
            elif e["name"] == "shoot":
                self.entities.append(Bullet(self, e["alliance"], e["pos"], e["dir"]))
            elif e["name"] == "call":
                scale = [0.5, 1]
                entities = []  # type: [Entity]
                pos = e["pos"]
                e_type = e["type"]

                for coord in self.radius_gen(pos, e["radius"]):  # type: Carrot
                    t = self.get_tile(coord)
                    if not t:
                        continue
                    # Debug.circle(Color("black"), (t.x + 0.5, t.y + 0.5), 0.25)

                    for ent in t.entities:
                        if ent.alliance != e["alliance"]:
                            continue

                        if e_type is SeedType.melee and type(ent) is Carrot:
                            entities.append(ent)
                        elif e_type is SeedType.ranged and type(ent) is Sprout:
                            entities.append(ent)

                counter = 0
                for delta in self.spiral_gen():
                    delta *= scale[e_type.value]

                    if counter >= len(entities):
                        break

                    t = self.get_tile(pos + delta)

                    if t and (not t.state or (t.state["name"] is TileState.blocked and t.state["entity"] in entities)):
                        entities[counter].call(pos + delta)
                        counter += 1
            elif e["name"] == "death":
                ent = e["author"]  # type: Entity
                ent.kill()

                if type(ent) is Player:
                    ent.spawn(self.respawn_time)
                else:
                    if ent in self.entities:
                        self.entities.remove(ent)

    def constrain_vector(self, pos: Vector2) -> Vector2:
        if pos.x < 0:
            pos.x = 0
        if pos.y < 0:
            pos.y = 0
        if pos.x >= WORLD_DIMENSION["width"]:
            pos.x = WORLD_DIMENSION["width"] - 0.001
        if pos.y >= WORLD_DIMENSION["height"]:
            pos.y = WORLD_DIMENSION["height"] - 0.001


def new_game() -> World:
    from game.input import lock_input
    from game.player import Player, SeedType
    from game.carrot import Carrot
    from game.sprout import Sprout

    world = World()
    players = lock_input()
    world.player_count = len(players)
    for i in players:
        world.players[i] = Player(world, i, Vector2(SPAWN_POSITIONS[i]))
        world.entities.append(world.players[i])

    for i in range(0):
        world.entities.append(Sprout(world, 0,
                                     Vector2(random() * WORLD_DIMENSION["width"],
                                             random() * WORLD_DIMENSION["height"])))

    for i in range(5):
        world.get_tile(Vector2(random() * WORLD_DIMENSION["width"],
                               random() * WORLD_DIMENSION["height"])).set_pickup(SeedType.melee, 5)
    #
    # for i in range(5):
    #     world.get_tile(Vector2(random() * WORLD_DIMENSION["width"],
    #                            random() * WORLD_DIMENSION["height"])).set_pickup(SeedType.ran, 5)

    return world


if __name__ == "__main__":

    world = World()

    for v in world.spiral_gen():  # type: Vector2
        print(v)

        if v.length_squared() > 100:
            break
