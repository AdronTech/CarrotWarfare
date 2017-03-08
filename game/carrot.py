from game.entity import *

class Carrot(Entity):

    def __init__(self, world: World, alliance, pos):
        super().__init__(world, alliance, pos)

        self.target = None
        self.state = None
        self.go_idle()

        self.speed = 3
        self.hp = 20

        self.attack_range = 1.5
        self.attack_angle = 45
        self.damage = 20

        self.sight_range = 4
        self.player_range = 0.1
        self.enemy_range = self.attack_range * 0.5

        self.enemies_in_sight = []  # type: list[Entity]

        self.look_timer = gen_timer(1)

    def update(self, input=None):
        super().update()
        if self.hard_lock > 0:
            return

        if self.target:
            self.dir = (self.target.pos - self.pos).normalize()

            if issubclass(type(self.target), Entity):
                if self.target.death_stamp:
                    self.go_idle()

        # print(self.state)

        # seeking
        if self.state is CarrotState.seek_pos or self.state is CarrotState.seek_enemy:

            dist = self.target.pos - self.pos  # type: Vector2

            if dist.length_squared() > 0.1**2:
                dist.scale_to_length(self.speed * delta_time)

                self.set_pos(self.pos + dist)

        # attack
        if self.state is CarrotState.attack:

            if self.soft_lock < 0:
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

            if self.target.death_stamp:
                self.state = CarrotState.idle

        # idle and seek enemy and attack
        if self.state is not CarrotState.seek_pos:
            if next(self.look_timer):
                self.look_around()

                if self.enemies_in_sight:
                    self.target = self.get_nearest_enemy()

            if self.target:
                if self.target.pos.distance_squared_to(self.pos) <= self.enemy_range**2:
                    self.state = CarrotState.attack
                else:
                    self.state = CarrotState.seek_enemy
            else:
                self.go_idle()

        #seek pos
        else:
            if self.target:
                if self.target.pos.distance_squared_to(self.pos) <= self.player_range:
                    self.go_idle()
            else:
                self.go_idle()

    def go_idle(self):
        self.target = None
        self.state = CarrotState.idle

    def look_around(self):
        self.enemies_in_sight = []

        for t in self.world.tile_radius(self.pos, self.sight_range):
            if not t:
                continue

            for e in t.entities:
                if e.alliance != self.alliance:
                    if e not in self.enemies_in_sight:
                        self.enemies_in_sight.append(e)

    def get_nearest_enemy(self) -> Entity:

        if not self.enemies_in_sight:
            return None

        index = 0

        for i in range(1, len(self.enemies_in_sight)):

            if self.enemies_in_sight[i].pos.distance_squared_to(self.pos) < self.enemies_in_sight[index].pos.distance_squared_to(self.pos):
                index = i

        return self.enemies_in_sight[index]

    def call(self, target: Vector2):
        self.target = TargetPosition(target)
        self.state = CarrotState.seek_pos


class TargetPosition:
     def __init__(self, pos: Vector2):
        self.pos = pos


class CarrotState(Enum):
    idle = 0
    seek_enemy = 1
    seek_pos = 2
    attack = 3
