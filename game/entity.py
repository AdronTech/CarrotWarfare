from pygame import math
from game.world import *
from game.tile import *

class Entity:
    def __init__(self, world: World, alliance, pos: math.Vector2 = math.Vector2()):
        self.pos = pos
        self.events = []
        self.world = world
        self.render_flags = {}
        self.alliance = alliance

    def update(self, events=None, input=None):
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
