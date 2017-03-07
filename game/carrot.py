from game.entity import Entity
from enum import Enum
from game.world import World
from game.player import Player

class Carrot(Entity):

    def __init__(self, world: World, player: Player):
        super().__init__(world)
        self.state = CarrotState.idle
        self.player = player

        self.sight_range = 4
        self.player_range = 1
        self.enemy_range = 1

        self.entities_in_sight = []

    def update(self):
        if self.state is CarrotState.idle:

            self.look_arround()

            if self.enemy_nearby():
                self.target = self.get_nearest_enemy()
                self.state = CarrotState.seek_enemy

    def look_arround(self):
        self.entities_in_sight = []

        myX = int(self.pos.x)
        myY = int(self.pos.y)

        for x in range(myX - self.sight_range, myX + self.sight_range + 1):
            for y in range(myY - self.sight_range, myY + self.sight_range + 1):
                if x - myX + y - myY > self.sight_range:
                    continue

                t = self.world.grid[myX][myY]
                self.entities_in_sight.extend(t.entities)

    def enemy_nearby(self):
        for e in self.entities_in_sight:
            if e is Carrot or (e is Player and e != self.player):
                return True

    def get_nearest_enemy(self):

        # TODO: find nearest
        pass


class CarrotState(Enum):
    idle = 0
    seek_enemy = 1
    seek_player = 2
    attack = 3
