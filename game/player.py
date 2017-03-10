from game.entity import *


class SeedType(Enum):
    melee = 0
    ranged = 1


class Player(Entity):
    def __init__(self, world: World, alliance, spawn: Vector2):
        super().__init__(world, alliance)

        self.seed_mode = SeedType.melee  # type: SeedType

        self.seeds = [0 for i in range(len(list(SeedType)))]
        self.seeds[SeedType.melee.value] = 5
        self.seeds[SeedType.ranged.value] = 5

        self.attack_range = 1.5
        self.attack_angle = 90
        self.damage = PLAYER_DAMAGE
        self.speed = 4

        self.spawnpoint = spawn
        self.respawn_timer = 0
        self.can_respawn = True

        self.spawn()

    def spawn(self, time=0):
        self.can_respawn = not time < 0
        self.respawn_timer = time

    def update(self, input=None):
        super().update()
        if self.hard_lock > 0:
            return

        if self.respawn_timer >= 0:
            self.respawn_timer -= delta_time

            if self.respawn_timer <= 0:
                self.death_stamp = None
                self.hp = PLAYER_LIFE
                self.set_pos(self.spawnpoint)

            return

        self.events.clear()

        for input_command in input:
            command = input_command["command"]
            if command == Commands.directional:
                self.move(input_command["dir"])

            if command == Commands.look:
                self.look(input_command["dir"])

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

    def move(self, dir: Vector2):

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

    def look(self, dir: Vector2):
        self.dir = dir

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
            # log
            self.events.append({
                "name": "plant_request",
                "pos": self.world.int_vec(self.pos),
                "type": self.seed_mode,
                "remaining": self.get_seeds()
            })
            self.world.events.append({
                "name": "plant_request",
                "tile": self.world.get_tile(self.pos),
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
            "type": self.seed_mode,
            "author": self
        })

    def swap(self):

        next = self.seed_mode.value
        # while True:
        next = (next + 1) % len(list(SeedType))
            # if next == self.seed_mode.value or self.seeds[next] != 0:
            #     break

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

    def set_seeds(self, amount, type: SeedType = None):
        if not type:
            type = self.seed_mode

        self.seeds[type.value] = amount

    def increase_seeds(self, amount=1, type: SeedType = None):
        if not type:
            type = self.seed_mode

            self.set_seeds(min(self.get_seeds(type) + amount, PLAYER_SEED_POUCH), type)

    def consume_seeds(self, amount=1, type: SeedType = None):

        if amount > self.get_seeds(type):
            return False

        if not type:
            type = self.seed_mode

        self.set_seeds(self.get_seeds(type) - amount, type)
        return True

    def pickup(self, seed_mode: SeedType, amount) -> bool:
        if self.get_seeds(seed_mode) + 1 <= PLAYER_SEED_POUCH:
            self.set_seeds(min(self.get_seeds(seed_mode) + amount, PLAYER_SEED_POUCH), seed_mode)

            # log
            self.events.append({
                "name": "pick_up",
                "seed": seed_mode,
                "amount": self.get_seeds(seed_mode),
                "delta": amount
            })
            return True
        else:
            return False


if __name__ == "__main__":
    world = World()

    player = Player(world)
    player.update(input=[{"command": Commands.directional, "value": Vector2(10, 20)},
                         {"command": Commands.swap},
                         {"command": Commands.swap}])

    print(player.events)
