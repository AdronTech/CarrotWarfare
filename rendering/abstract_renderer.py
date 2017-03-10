from pygame import Surface, draw, Rect
from pygame.transform import *
from pygame.gfxdraw import aacircle, aatrigon, filled_circle, filled_trigon, arc
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
from random import randint, random, randrange


class AbstractRenderer:

    def __init__(self, target_resolution):
        self.arena_surface_offset = (0, 0)
        self.target_resolution = target_resolution

    def render(self, target: Surface, world):
        pass

    def world_to_screen(self, v):
        x, y = (Vector2(v * TILE_SIZE) + Vector2(self.arena_surface_offset))


        return Vector2(floor(x * self.target_resolution[0] / RENDER_RESOLUTION[0]), floor(y * self.target_resolution[1] / RENDER_RESOLUTION[1]))

    def screen_to_world(self, v):
        v = Vector2(v.x * RENDER_RESOLUTION[0] / self.target_resolution[0], v.y * RENDER_RESOLUTION[1] / self.target_resolution[1])
        v -= Vector2(self.arena_surface_offset)
        return v / TILE_SIZE
