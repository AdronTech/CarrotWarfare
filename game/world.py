from game.input import get
from game.tile import Tile

WORLD_DIMENSION = (20, 20)


class World:
    def __init__(self):
        self.player_count = 0
        self.grid = [[Tile() for i in range(WORLD_DIMENSION[1])] for j in range(WORLD_DIMENSION[0])]  # type: [[Tile]]
        self.entities = []
        self.events = []

    def update(self):
        commands = get()
        # update each entity
        for e in self.entities:
            e.update()
