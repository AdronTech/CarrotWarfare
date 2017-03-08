from game.input import *
from game.tile import *
from timing import *
from random import random, randint
from rendering import debugger as Debug
from pygame import Color

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
        self.grid = [[Tile(self.events, x, y) for y in range(h)] for x in range(w)]  # type: [[Tile]]

    def radius_gen(self, pos, r):
        for dx in range(-r, r + 1):
            for dy in range(-(r - abs(dx)), r - abs(dx) + 1):
                yield Vector2(pos) + Vector2(dx, dy)

    def get_tile(self, pos):
        x, y = pos

        x = int(x)
        y = int(y)

        if x < 0 or y < 0 or x >= WORLD_DIMENSION["width"] or y >= WORLD_DIMENSION["height"]:
            return None

        return self.grid[x][y]

    def update(self):

        self.events.clear()
        commands = get_input()  # type: [[], [], [], []]

        deaths = []

        for i in range(len(self.growing)):
            self.growing[i].update()

        for i in range(self.player_count):
            ent = self.entities[i]  # type: Entity
            ent.update(commands[i])
            if ent.death_stamp and now() - ent.death_stamp > 1000:
                ent.death_stamp = None

        for i in range(self.player_count, len(self.entities)):
            ent = self.entities[i]  # type: Entity
            ent.update()
            if ent.death_stamp and now() - ent.death_stamp > 0:
                deaths.append(ent)

        for e in deaths:
            self.entities.remove(e)

        # for col in self.grid:
        #     for t in col:
        #         if [(e.death_stamp) for e in t.entities if e.death_stamp]:
        #             Debug.circle((0, 0, 0, 255), (t.x + 0.5, t.y + 0.5), 0.2)

        self.check_events()

        # print(self.events)

    def check_events(self):
        from game.carrot import Carrot
        from game.player import Player

        for e in self.events:  # type: dict
            if e["name"] == "plant":
                t = self.grid[e["pos"]["x"]][e["pos"]["y"]]
                self.growing.append(t)
                t.plant(e["type"], e["alliance"])
            elif e["name"] == "full_grown":
                self.growing.remove(e["tile"])
                self.entities.append(Carrot(self, e["alliance"], e["pos"]))
            elif e["name"] == "attack":
                pos = e["pos"]  # type: Vector2
                dir = e["dir"]
                r = e["range"]
                h_angle = e["angle"] / 2

                possible_enemies = []  # type: Entity

                for x in range(int(e["pos"].x - r), int(e["pos"].x + r + 1)):
                    for y in range(int(e["pos"].y - r), int(e["pos"].y + r + 1)):
                        if x < 0 or y < 0 or x >= WORLD_DIMENSION["width"] or y >= WORLD_DIMENSION["height"]:
                            continue
                        for ent in self.grid[x][y].entities:  # type: Entity
                            if e["alliance"] != ent.alliance and (type(ent) is Carrot or type(ent) is Player):
                                dist = ent.pos - pos  # type: Vector2

                                if dist.length_squared() > r ** 2:
                                    continue

                                if dist.angle_to(dir) > h_angle:
                                    continue

                                possible_enemies.append((dist.length_squared(), ent))

                possible_enemies = sorted(possible_enemies, key = lambda entity: entity[0])  # sort by distance
                for i in range(min(e["count"], len(possible_enemies))):
                    possible_enemies[i][1].hit(e["damage"])
                    Debug.circle(Color("blue"),possible_enemies[i][1].pos, 0.2)

            elif e["name"] == "call":
                for coord in self.radius_gen(e["pos"], e["radius"]):  # type: Carrot
                    t = self.get_tile(coord)
                    if t:
                        # Debug.circle(Color("black"), (t.x + 0.5, t.y + 0.5), 0.25)

                        for ent in t.entities:
                            if type(ent) is not Carrot:
                                continue
                            if ent.alliance != e["alliance"]:
                                continue

                            ent.call(e["pos"])

            elif e["name"] == "player_death":
                e["author"].spawn()

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
    from game.player import Player
    from game.carrot import Carrot

    world = World()
    world.player_count = lock_input()
    for i in range(world.player_count):
        world.entities.append(Player(world, i, Vector2(SPAWN_POSITIONS[i])))

    for i in range(0):
        world.entities.append(Carrot(world, randint(0, 3),
                                     Vector2(random() * WORLD_DIMENSION["width"],
                                             random() * WORLD_DIMENSION["height"])))

    return world


if __name__ == "__main__":

    world = World()

    for i in world.tile_radius((0, 0), 4):
        print(i)
