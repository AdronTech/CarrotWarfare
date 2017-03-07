from enum import Enum

from game.entity import Entity
from game.commands import Commands
from game.world import World
from game.tile import Tile
from timing import *
from pygame import *


class SeedMode(Enum):
    melee = 0
    ranged = 1


class Player(Entity):
    def __init__(self, world: World, alliance, spawn: math.Vector2):
        super().__init__(world, alliance)

        self.seed_mode = SeedMode.melee  # type: SeedMode

        self.seeds = [0 for i in range(len(list(SeedMode)))]
        self.seeds[SeedMode.melee.value] = 200
        self.seeds[SeedMode.ranged.value] = 200

        self.attack_range = 1.5
        self.attack_angle = 45
        self.damage = 10
        self.speed = 5

        self.spawnpoint = spawn

        self.spawn()

    def update(self, input=None):

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

                # if self.events:
                #     print(self.events)

    def spawn(self):
        self.set_pos(self.spawnpoint)
        self.hp = 40

    def move(self, input: math.Vector2):
        # calc delta pos
        d_pos = input * self.speed * delta_time  # type: math.Vector2

        self.dir = input

        # move
        self.set_pos(self.pos + d_pos)

        # log
        self.events.append({
            "name": "move",
            "delta": d_pos,
            "pos": self.pos
        })

    def attack(self):

        # TODO: attack enemy

        # log
        self.events.append({
            "name": "attack"
        })
        self.world.events.append({
            "name": "attack",
            "pos": self.pos,
            "dir": self.dir,
            "range": self.attack_range,
            "angle": self.attack_angle,
            "alliance": self.alliance,
            "damage": self.damage,
            "author": self
        })

    def plant(self):
        if self.get_seeds() > 0:
            plant_pos = {"x": int(self.pos.x), "y": int(self.pos.y)}

            t = self.world.grid[plant_pos["x"]][plant_pos["y"]]  # type: Tile
            if not t.state:
                self.seeds[self.seed_mode.value] -= 1

                # log
                self.events.append({
                    "name": "plant",
                    "pos": plant_pos,
                    "type": self.seed_mode,
                    "remaining": self.get_seeds()
                })
                self.world.events.append({
                    "name": "plant",
                    "pos": plant_pos,
                    "type": self.seed_mode,
                    "alliance": self.alliance,
                    "author": self
                })

    def call(self):

        # TODO: call carrots

        # log
        self.events.append({
            "name": "call"
        })
        self.world.events.append({
            "name": "call",
            "pos": self.pos,
            "alliance": self.pos,
            "author": self
        })

    def swap(self):

        next = self.seed_mode.value
        while True:
            next = (next + 1) % len(list(SeedMode))
            if next == self.seed_mode.value or self.seeds[next] != 0:
                break

        self.seed_mode = SeedMode(next)

        # log
        self.events.append({
            "name": "swap",
            "mode": self.seed_mode,
            "amount": self.get_seeds()
        })

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
