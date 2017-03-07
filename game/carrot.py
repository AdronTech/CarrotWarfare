from game.entity import Entity
from enum import Enum
from game.world import World
from game.player import Player


class Carrot(Entity):

    def __init__(self, world: World, player: Player, pos):
        super().__init__(world, pos)
        self.state = CarrotState.idle
        self.player = player

        self.sight_range = 4
        self.player_range = 1
        self.enemy_range = 1

        self.entities_in_sight = []  # type: list[Entity]
        self.target = self  # type: Entity

    def update(self, events=None, input=None):
        if self.state is CarrotState.idle:

            self.look_around()

            if self.enemy_nearby():
                self.target = self.get_nearest_enemy()
                if self.target:
                    self.state = CarrotState.seek_enemy

        elif self.state is CarrotState.seek_enemy:
            if self.target:
                self.target.


    def look_around(self):
        self.entities_in_sight = []

        my_x = int(self.pos.x)
        my_y = int(self.pos.y)

        for x in range(my_x - self.sight_range, my_x + self.sight_range + 1):
            for y in range(my_y - self.sight_range, my_y + self.sight_range + 1):
                if x - my_x + y - my_y > self.sight_range:
                    continue

                t = self.world.grid[my_x][my_y]
                self.entities_in_sight.extend(t.entities)

    def enemy_nearby(self):
        for e in self.entities_in_sight:
            if e is Carrot or (e is Player and e != self.player):
                return True

    def get_nearest_enemy(self):
        if not self.entities_in_sight:
            return None

        index = 0
        for i in range(1, len(self.entities_in_sight)):
            if self.entities_in_sight[i].pos.distance_squared_to(self.pos) < self.entities_in_sight[index].pos.distance_squared_to(self.pos):
                index = i

        return index

    def call(self):
        self.target = self.player
        self.state = CarrotState.seek_player


class CarrotState(Enum):
    idle = 0
    seek_enemy = 1
    seek_player = 2
    attack = 3
