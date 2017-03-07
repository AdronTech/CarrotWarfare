from enum import Enum

class Tile:
    def __init__(self):
        self.entities = []
        self.state = None  # TileState
        self.render_flags = {}

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

    def set_pickup(self, seed_mode):
        self.state = {"name": TileState.pick_up,
                      "seed": seed_mode}

class TileState(Enum):
    pick_up = 0
    growing = 1
