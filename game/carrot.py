from game.entity import *


class Carrot(Entity):
    def __init__(self, world: World, alliance, pos):
        super().__init__(world, alliance, pos)

        self.target = None
        self.state = None
        self.go_idle()

        self.speed = 10
        self.hp = 30

        self.attack_range = 1.5
        self.attack_angle = 45
        self.damage = 1

        self.sight_range = 4
        self.player_range = 1
        self.enemy_range = self.attack_range * 0.75

        self.enemies_in_sight = []  # type: list[Entity]

        self.look_timer = gen_timer(0.5)

        self.vel = Vector2()
        self.acc = Vector2()

    def update(self, input=None):
        super().update()
        if self.hard_lock > 0:
            return

        # Debug.line(Color("black"), self.pos, self.pos + self.vel)
        # for coord in self.world.radius_gen(self.pos, self.sight_range):
        #     t = self.world.get_tile(coord)  # type: Tile
        #     if t:
        #         Debug.rect(Color("black"), ((t.x,t.y), (0.2, 0.2)))
        #
        # if self.state is CarrotState.idle:
        #     Debug.circle((0, 0, 0), self.pos, 0.5)
        # elif self.state is CarrotState.attack:
        #     Debug.circle((0, 255, 255), self.pos, 0.5)
        # elif self.state is CarrotState.seek_pos:
        #     Debug.circle((255, 0, 255), self.pos, 0.5)
        # elif self.state is CarrotState.seek_enemy:
        #     Debug.circle((255, 255, 0), self.pos, 0.5)

        if self.target:
            # Debug.line((0, 0, 0), self.pos, self.target.pos)

            if issubclass(type(self.target), Entity):
                if self.target.death_stamp:
                    self.go_idle()

            des_dir = Vector2(1, 0)
            if self.state is CarrotState.seek_enemy or self.state is CarrotState.seek_pos:
                des_dir = (self.vel + Vector2(0, 0.001)).normalize()
            elif self.state is CarrotState.attack:
                des_dir = (self.target.pos - self.pos).normalize()  # type: Vector2

            self.dir += (des_dir - self.dir) * delta_time * 5

        # seeking
        if self.state is CarrotState.seek_pos or self.state is CarrotState.seek_enemy:
            des_vel = self.target.pos - self.pos  # type: Vector2
            des_vel *= 2
            force = des_vel - self.vel  # type: Vector2

            self.acc += force

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
                    "count": 2,
                    "author": self
                })

            if self.target.death_stamp:
                self.go_idle()

        # idle and seek enemy and attack
        if self.state is not CarrotState.seek_pos:
            if next(self.look_timer):
                self.look_around()

                if self.enemies_in_sight:
                    self.target = self.get_nearest_enemy()

            if self.target:
                if self.target.pos.distance_squared_to(self.pos) <= self.enemy_range ** 2:
                    self.state = CarrotState.attack
                else:
                    self.state = CarrotState.seek_enemy
            else:
                self.go_idle()

                # seek pos
        else:
            if self.target:
                if self.target.pos.distance_squared_to(self.pos) <= self.player_range:
                    self.go_idle()
            else:
                self.go_idle()

        self.vel = self.vel + self.acc * delta_time
        self.set_pos(self.pos + self.vel * delta_time)

        if self.vel.length_squared() > self.speed ** 2:
            self.vel.scale_to_length(self.speed)
        self.acc = Vector2()

    def go_idle(self):
        self.target = None
        self.state = CarrotState.idle
        self.vel = Vector2()

    def look_around(self):
        self.enemies_in_sight = []

        for coord in self.world.radius_gen(self.pos, self.sight_range):
            t = self.world.get_tile(coord)
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

            if self.enemies_in_sight[i].pos.distance_squared_to(self.pos) < self.enemies_in_sight[
                index].pos.distance_squared_to(self.pos):
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
