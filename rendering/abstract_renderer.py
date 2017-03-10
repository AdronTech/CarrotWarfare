from pygame import Surface, draw, Rect
from pygame.transform import *
from pygame.gfxdraw import aacircle, aatrigon, filled_circle, filled_trigon
from rendering.constants import *
from pygame.math import Vector2
from math import floor
from game.tile import Tile
from game.world import World
from game.entity import Entity
from game.carrot import Carrot
from game.sprout import Sprout, SproutState
from game.bullet import Bullet
from game.player import Player, SeedType
from rendering.loader import load_all
from game.constants import *



class AbstractRenderer:

    def __init__(self):
        self.arena_surface_offset = (0, 0)

    def render(self, target: Surface, world):
        pass

    def world_to_screen(self, v):
        x, y = (Vector2(v * TILE_SIZE) + Vector2(self.arena_surface_offset))
        return Vector2(floor(x), floor(y))

    def screen_to_world(self, v):
        v -= Vector2(self.arena_surface_offset)
        return v / TILE_SIZE
