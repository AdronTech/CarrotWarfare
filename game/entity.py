from pygame import math
from game.world import *
from game.tile import *


class Entity:
    def __init__(self, world: World, alliance, pos: math.Vector2 = math.Vector2(), hp=0):
        self.pos = pos

        self.events = []
        self.world = world
        self.render_flags = {}
        self.alliance = alliance
        self.dir = math.Vector2(1, 0);
        self.hp = hp

        t = self.world.grid[int(self.pos.x)][int(self.pos.y)]  # type: Tile
        t.register(self)

    def update(self, input=None):
        pass

    def set_pos(self, pos: math.Vector2):

        # unregister
        t = self.world.grid[int(self.pos.x)][int(self.pos.y)]  # type: Tile
        t.unregister(self)

        self.pos = pos

        # constrain
        if pos.x < 0:
            pos.x = 0
        if pos.y < 0:
            pos.y = 0
        if pos.x >= WORLD_DIMENSION["width"]:
            pos.x = WORLD_DIMENSION["width"] - 0.001
        if pos.y >= WORLD_DIMENSION["height"]:
            pos.y = WORLD_DIMENSION["height"] - 0.001

        # register
        t = self.world.grid[int(self.pos.x)][int(self.pos.y)]  # type: Tile
        t.register(self)

    def hit(self, damage):
        self.hp -= damage

        print("hit", self)
        # TODO: hit and death log

        self.events.append({
            "name": "hit",
            "damage": damage,
            "remaining": self.hp
        })

        if self.hp < 0:
            self.hp = 0
            self.world.events.append({
                "name": "death",
                "author": self
            })
