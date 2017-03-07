from game.input import get
from game.tile import Tile

WORLD_DIMENSION = {"width": 20, "height": 20}


class World:
    def __init__(self):
        self.player_count = 0
        w = WORLD_DIMENSION["width"]
        h = WORLD_DIMENSION["height"]
        self.grid = [[Tile() for i in range(w)] for j in range(h)]  # type: [[Tile]]
        self.entities = []
        self.events = []

    def update(self):
        commands = get()  # type: [[][][][]]
        # update each entity
        for e in self.entities:
            e.update()
