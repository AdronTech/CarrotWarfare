from pygame import Surface, draw, Rect
from pygame.gfxdraw import aacircle, aatrigon, filled_circle, filled_trigon
from rendering.constants import *
from game.tile import Tile
from game.world import World
from game.entity import Entity
from game.carrot import Carrot
from game.sprout import Sprout, SproutState
from game.player import Player, SeedType
from rendering.loader import load_all
from game.constants import *


class AbstractRenderer:
    def render(self, target: Surface, world):
        pass
