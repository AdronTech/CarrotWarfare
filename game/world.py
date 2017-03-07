from game.input import get_input
from game.input import lock_input
from game.tile import Tile, TileState
from random import random, randint

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
        self.grid = [[Tile() for i in range(h)] for j in range(w)]  # type: [[Tile]]
        self.entities = []
        self.events = []

    def update(self):
        self.events = []
        commands = get_input()  # type: [[], [], [], []]
        for i in range(self.player_count):
            self.entities[i].update(commands[i])
        for i in range(self.player_count, len(self.entities)):
            self.entities[i].update()

        self.check_events()

    def check_events(self):
        for e in self.events:
            if e["name"] == "plant":
                self.grid[e["pos"]["x"]][e["pos"]["y"]].plant(e["type"], e["alliance"])
                print("huii")
            if e["name"] == "attack":
                # TODO: attack
                pass

def new_game() -> World:
    from game.carrot import Carrot
    from game.player import Player
    from pygame.math import Vector2
    world = World()
    world.player_count = lock_input()
    for i in range(world.player_count):
        world.entities.append(Player(world, i, Vector2() + SPAWN_POSITIONS[i]))

    # for i in range(100):
    #     world.entities.append(Carrot(world, randint(0, 3), Vector2(random()*WORLD_DIMENSION["width"], random() * WORLD_DIMENSION["height"])))
    return world
