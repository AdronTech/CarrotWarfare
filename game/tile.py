from enum import Enum

from pygame.math import Vector2
from timer import gen_timer


class Tile:
    def __init__(self, worldevents, x, y):
        self.entities = []
        self.collider = []
        self.state = None  # TileState
        self.render_flags = {}
        self.timer = None
        self.worldevents = worldevents
        self.x = x
        self.y = y

    def update(self):
        if self.state and self.state["name"] == TileState.growing and next(self.timer):
            self.state["g_state"] += 1

            if self.state["g_state"] == 5:
                self.worldevents.append({
                    "name": "full_grown",
                    "pos": Vector2(self.x + 0.5, self.y + 0.5),
                    "type": self.state["seed"],
                    "alliance": self.state["alliance"],
                    "tile": self
                })
                self.state = None

    def register(self, entity):
        if entity not in self.entities:
            self.entities.append(entity)

        from game.player import Player
        if type(entity) is Player:
            if self.state and self.state["name"] == TileState.pick_up:

                if entity.pickup(self.state["seed"], self.state["amount"]):
                    self.worldevents.append({
                        "name": "pick_up",
                        "type": self.state["seed"],
                        "alliance": entity.alliance,
                        "tile": self
                    })
                    self.state = None

    def unregister(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def reg_coll(self, entity):
        if entity not in self.collider:
            self.collider.append(entity)

    def unreg_coll(self, entity):
        if entity in self.collider:
            self.collider.remove(entity)

    def block(self, entity):
        self.state = {"name": TileState.blocked,
                      "entity": entity}

    def unblock(self, entity):
        if self.state and self.state["name"] is TileState.blocked and self.state["entity"] is entity:
            self.state = None

    def plant(self, seed_type, alliance):
        self.state = {"name": TileState.growing,
                      "seed": seed_type,
                      "alliance": alliance,
                      "g_state": 1}
        self.timer = gen_timer(1)

    def set_pickup(self, seed_mode, amount):
        self.state = {"name": TileState.pick_up,
                      "seed": seed_mode,
                      "amount": amount}


class TileState(Enum):
    pick_up = 0
    growing = 1
    blocked = 2
