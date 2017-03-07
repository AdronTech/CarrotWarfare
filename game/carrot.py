from enum import Enum
from pygame import *
import timing
from game.entity import Entity
from game.world import World
from game.player import Player


class Carrot(Entity):

    def __init__(self, world: World, alliance, pos):
        super().__init__(world, alliance, pos)
        self.state = CarrotState.idle

        self.speed = 5

        self.sight_range = 4
        self.player_range = 1
        self.enemy_range = 1

        self.target = self  # type: Entity
        self.entities_in_sight = []  # type: list[Entity]

    def update(self, events=None, input=None):

        # seeking
        if self.state is CarrotState.seek_pos or self.state is CarrotState.seek_enemy:
            dir = self.target.pos - self.pos  # type: math.Vector2
            dir.scale_to_length(self.speed * timing.delta_time)

            self.set_pos(self.pos + dir)

        # idle
        if self.state is CarrotState.idle:
            self.look_around()

            if self.enemy_nearby():
                self.target = self.get_nearest_enemy()
                if self.target:
                    self.state = CarrotState.seek_enemy
        # seek enemy
        elif self.state is CarrotState.seek_enemy:
            if self.target:
                if self.target.pos.distance_squared_to(self.pos) <= self.enemy_range:
                    self.state = CarrotState.attack
            else:
                self.state = CarrotState.idle

        elif self.state is CarrotState.seek_pos:
            if self.target:
                if self.target.pos.distance_squared_to(self.pos) <= self.player_range:
                    self.state = CarrotState.idle
            else:
                self.state = CarrotState.idle

        # attack
        elif self.state is CarrotState.attack:
            if not self.target:
                self.state = CarrotState.idle

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
            if (type(e) is Carrot or type(e) is Player) and e.alliance != self.alliance:
                return True

    def get_nearest_enemy(self) -> Entity:
        enemies_in_sight =[]

        # get all enemies
        for e in self.entities_in_sight:
            if (type(e) is Carrot or type(e) is Player) and e.alliance != self.alliance:
                enemies_in_sight.append(e)

        if not enemies_in_sight:
            return None

        index = 0

        for i in range(1, len(enemies_in_sight)):

            if enemies_in_sight[i].pos.distance_squared_to(self.pos) < enemies_in_sight[index].pos.distance_squared_to(self.pos):
                index = i

        return enemies_in_sight[index]

    def call(self, target: Entity):
        self.target = target
        self.state = CarrotState.seek_pos


class CarrotState(Enum):
    idle = 0
    seek_enemy = 1
    seek_pos = 2
    attack = 3
