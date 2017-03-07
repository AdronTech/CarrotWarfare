from enum import Enum
from timer import gen_timer
from game.world import World
from pygame import *


class Tile:
    def __init__(self, world: World, x, y):
        self.entities = []
        self.state = None  # TileState
        self.render_flags = {}
        self.timer = None
        self.world = world
        self.x = x
        self.y = y

    def update(self):
        if self.state and self.state["name"] == TileState.growing and next(self.timer):
            self.state["g_state"] += 1

            if self.state["g_state"] == 5:
                self.world.events.append({
                    "name": "full_grown",
                    "pos": math.Vector2(self.x + 0.5, self.y + 0.5),
                    "type": self.state["seed"],
                    "alliance": self.state["alliance"],
                    "tile": self
                })
                self.state = None

    def register(self, entity):
        self.entities.append(entity)

    def unregister(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def plant(self, seed_mode, alliance):
        self.state = {"name": TileState.growing,
                      "seed": seed_mode,
                      "alliance": alliance,
                      "g_state": 1}
        self.timer = gen_timer(1)

    def set_pickup(self, seed_mode):
        self.state = {"name": TileState.pick_up,
                      "seed": seed_mode}


class TileState(Enum):
    pick_up = 0
    growing = 1
