from game.entity import *


class SeedType(Enum):
    melee = 0
    ranged = 1


class Player(Entity):
    def __init__(self, world: World, alliance, spawn: Vector2):
        super().__init__(world, alliance)

        self.seed_mode = SeedType.melee  # type: SeedType

        self.seeds = [0 for i in range(len(list(SeedType)))]
        self.seeds[SeedType.melee.value] = 200
        self.seeds[SeedType.ranged.value] = 200

        self.attack_range = 1.5
        self.attack_angle = 90
        self.damage = 5
        self.speed = 5

        self.spawnpoint = spawn

        self.spawn()

    def spawn(self):
        self.set_pos(self.spawnpoint)
        self.hp = 100

    def update(self, input=None):
        super().update()
        if self.hard_lock > 0:
            return

        self.events.clear()

        for input_command in input:
            command = input_command["command"]
            if command == Commands.directional:
                self.move(input_command["dir"], input_command["hold_position"])

            elif self.soft_lock <= 0:
                if command == Commands.attack:
                    self.attack()

                elif command == Commands.plant:
                    self.plant()

                elif command == Commands.call:
                    self.call()

                elif command == Commands.swap:
                    self.swap()

            # if self.events:
            #     print(self.events)

    def move(self, dir: Vector2, hold_pos: bool):

        self.dir = dir

        if hold_pos:
            return

        # calc delta pos
        d_pos = dir * self.speed * delta_time  # type: Vector2

        # move
        self.set_pos(self.pos + d_pos)

        # log
        self.events.append({
            "name": "move",
            "delta": d_pos,
            "pos": self.pos
        })

    def attack(self):

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
            "count": 5,
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
        # log
        self.events.append({
            "name": "call"
        })
        self.world.events.append({
            "name": "call",
            "pos": self.pos,
            "alliance": self.alliance,
            "radius": 7,
            "author": self
        })

    def swap(self):

        next = self.seed_mode.value
        while True:
            next = (next + 1) % len(list(SeedType))
            if next == self.seed_mode.value or self.seeds[next] != 0:
                break

        self.seed_mode = SeedType(next)

        # log
        self.events.append({
            "name": "swap",
            "mode": self.seed_mode,
            "amount": self.get_seeds()
        })

    def get_seeds(self, type: SeedType = None):
        if not type:
            type = self.seed_mode

        return self.seeds[type.value]

    def death(self):
        self.world.events.append({
            "name": "player_death",
            "alliance": self.alliance,
            "stamp": self.death_stamp,
            "author": self
        })

    def pickup(self, seed_mode: SeedType):
        self.seeds[seed_mode] += 1
        # log
        self.events.append({
            "name": "pick_up",
            "seed": seed_mode
        })


if __name__ == "__main__":
    world = World()

    player = Player(world)
    player.update(input=[{"command": Commands.directional, "value": Vector2(10, 20)},
                         {"command": Commands.swap},
                         {"command": Commands.swap}])

    print(player.events)
