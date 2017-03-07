from game.input import get_input
from game.input import lock_input
from random import random, randint
from pygame.math import Vector2

WORLD_DIMENSION = {"width": 27, "height": 17}
SPAWN_POSITIONS = [(1, 1),
                   (WORLD_DIMENSION["width"] - 1, 1),
                   (1, WORLD_DIMENSION["height"] - 1),
                   (WORLD_DIMENSION["width"] - 1, WORLD_DIMENSION["height"] - 1)]


class World:

    def __init__(self):
        from game.tile import Tile

        self.player_count = 0
        w = WORLD_DIMENSION["width"]
        h = WORLD_DIMENSION["height"]
        self.grid = [[Tile(self, x, y) for y in range(h)] for x in range(w)]  # type: [[Tile]]
        self.entities = []
        self.events = []
        self.growing = []  # type: [Tile]

    def update(self):
        self.events = []
        commands = get_input()  # type: [[], [], [], []]
        for i in range(len(self.growing)):
            self.growing[i].update()
        for i in range(self.player_count):
            self.entities[i].update(commands[i])
        for i in range(self.player_count, len(self.entities)):
            self.entities[i].update()

        self.check_events()

        # print(self.events)

    def check_events(self):
        from game.carrot import Carrot
        from game.entity import Entity
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
                h_angle = e["angle"]/2

                for x in range(int(e["pos"].x - r), int(e["pos"].x + r + 1)):
                    for y in range(int(e["pos"].y - r), int(e["pos"].y + r + 1)):
                        if x < 0 or y < 0 or x >= WORLD_DIMENSION["width"] or y >= WORLD_DIMENSION["height"]:
                            continue
                        for ent in self.grid[x][y].entities:  # type: Entity
                            if e["alliance"] != ent.alliance and (type(ent) is Carrot or type(ent) is Player):
                                dist = ent.pos - pos  # type: Vector2

                                if dist.length_squared() > r**2:
                                    continue

                                if dist.angle_to(dir) > h_angle:
                                    continue

                                ent.hit(e["damage"])

            elif e["name"] == "death":
                ent = e["author"]
                if type(ent) is Carrot:
                    if ent in self.entities:
                        self.entities.remove(ent)

                elif type(ent) is Player:
                    ent.spawn()  # type: Player

def new_game() -> World:
    from game.carrot import Carrot
    from game.player import Player
    from pygame.math import Vector2
    world = World()
    world.player_count = lock_input()
    for i in range(world.player_count):
        world.entities.append(Player(world, i, Vector2(SPAWN_POSITIONS[i])))

    # for i in range(100):
    #     world.entities.append(Carrot(world, randint(0, 3), Vector2(random()*WORLD_DIMENSION["width"], random() * WORLD_DIMENSION["height"])))
    return world
