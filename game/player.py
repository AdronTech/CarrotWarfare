from enum import Enum

from game.entity import Entity
from game.commands import Commands
from game.world import World
from timing import *
from pygame import *


class SeedMode(Enum):
    melee = 0
    ranged = 1


class Player(Entity):

    def __init__(self, world: World, pos: math.Vector2):
        super().__init__(world, pos)

        self.seed_mode = SeedMode.melee  # type: SeedMode
        self.seeds = [0 for i in range(len(list(SeedMode)))]
        # self.seeds[SeedMode.melee.value] = 20
        # self.seeds[SeedMode.ranged.value] = 10
        self.speed = 10

    def update(self, events=None, input=None):

        self.events = []

        for input_command in input:
            command = input_command["command"]
            if command == Commands.directional:
                self.move(input_command["value"])

            elif command == Commands.attack:
                self.attack()

            elif command == Commands.plant:
                self.plant()

            elif command == Commands.call:
                self.call()

            elif command == Commands.swap:
                self.swap()

    def move(self, input: math.Vector2):
        # calc delta pos
        d_pos = input * self.speed * delta_time

        # move
        self.set_pos(self.pos + d_pos)

        #log
        self.events.append({"name": "move",
                            "delta": d_pos,
                            "pos": self.pos})

    def attack(self):

        # TODO: attack enemy

        # log
        self.events.append({"name": "attack"})

    def plant(self):
        if self.get_seeds() > 0:
            plant_pos = {"x": int(self.pos.x), "y": int(self.pos.y)}

            # TODO: plant the plant

            # log
            self.events.append({"name": "plant",
                                "pos": plant_pos,
                                "type": self.seed_mode,
                                "remaining": self.get_seeds()})

    def call(self):

        # TODO: call carrots

        # log
        self.events.append({"name": "call"})

    def swap(self):

        next = self.seed_mode.value
        while True:
            next = (next + 1) % len(list(SeedMode))
            if next == self.seed_mode.value or self.seeds[next] != 0:
                break

        self.seed_mode = SeedMode(next)

        # log
        self.events.append({"name": "swap",
                            "mode": self.seed_mode,
                            "amount": self.get_seeds()})

    def get_seeds(self, type: SeedMode = None):
        if not type:
            type = self.seed_mode

        return self.seeds[type.value]

if __name__ == "__main__":
    world = World()

    player = Player(world)
    player.update(input=[{"command": Commands.directional, "value": math.Vector2(10, 20)},
                         {"command": Commands.swap},
                         {"command": Commands.swap}])

    print(player.events)
