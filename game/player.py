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

    def __init__(self, world: World):
        super().__init__(world)

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
                            "delta": d_pos})

    def attack(self):
        # log
        self.events.append({"name": "attack"})

    def plant(self):
        # log
        self.events.append({"name": "plant"})

    def call(self):
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
                            "amount": self.seeds[self.seed_mode.value]})

if __name__ == "__main__":
    world = World()

    player = Player(world)
    player.update(input=[{"command": Commands.directional, "value": math.Vector2(10, 20)},
                         {"command": Commands.swap},
                         {"command": Commands.swap}])

    print(player.events)
