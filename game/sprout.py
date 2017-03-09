from game.entity import *


class Sprout(Entity):
    def __init__(self, world: World, alliance, pos):
        super().__init__(world, alliance, pos)

        self.target = None
        self.state = None
        self.call(self.pos)

        self.speed = 1.3
        self.hp = 30

        self.turn_speed = 5

        self.damage = 1
        self.attack_angle = 20
        self.sight_range = 7

        self.enemies_in_sight = []  # type: list[Entity]

        self.look_timer = gen_timer(0.5)

        self.pos_range = 0.1

        self.wait_timer = 0

        self.vel = Vector2()

    def update(self, input=None):
        super().update()
        if self.hard_lock > 0:
            return

        # Debug.line(Color("black"), self.pos, self.pos + self.vel)
        # for coord in self.world.radius_gen(self.pos, self.sight_range):
        #     t = self.world.get_tile(coord)  # type: Tile
        #     if t:
        #         Debug.rect(Color("black"), ((t.x + 0.4, t.y + 0.4), (0.2, 0.2)))

        if self.target:
            if issubclass(type(self.target), Entity):
                if self.target.death_stamp:
                    self.go_idle()

            des_dir = Vector2(1, 0)
            if self.state is SproutState.seek_pos:
                des_dir = (self.vel + Vector2(0, 0.001)).normalize()
            elif self.state is SproutState.attack:
                des_dir = (self.target.pos - self.pos).normalize()  # type: Vector2

            self.dir += (des_dir - self.dir) * delta_time * self.turn_speed
            self.dir.normalize_ip()

        # seeking
        if self.state is SproutState.seek_pos:
            des_vel = self.target.pos - self.pos  # type: Vector2

            l2 = des_vel.length_squared()

            if l2 >= 0.0001:
                des_vel.scale_to_length(self.speed)
                self.vel = des_vel

                self.events.append({
                    "name": "move"
                })

            self.set_pos(self.pos + self.vel * delta_time)

        # wait
        if self.state is SproutState.wait:
            if self.wait_timer >= 0:
                self.wait_timer -= delta_time

                if self.wait_timer <= 0:
                    for delta in self.world.spiral_gen():
                        if abs(int(delta.x)) + abs(int(delta.y)) > self.sight_range:
                            self.go_wait(1)
                            break

                        t = self.world.get_tile(self.pos + delta)
                        if t and not t.state:
                            self.call(self.pos + delta)
                            break

        # attack
        if self.state is SproutState.attack:

            if self.soft_lock < 0:

                shoot_dir = self.target.pos - self.pos  # type: Vector2

                if abs(self.dir.angle_to(shoot_dir)) <= self.attack_angle / 2:
                    self.world.events.append({
                        "name": "shoot",
                        "pos": self.pos,
                        "dir": self.dir,
                        "alliance": self.alliance,
                        "author": self
                    })

                    self.events.append({
                        "name": "attack"
                    })

                    self.soft_lock = 1

            dx, dy = (self.world.int_vec(self.pos) - self.world.int_vec(self.target.pos))

            if self.target.death_stamp or abs(dx) + abs(dy) > self.sight_range:
                self.go_idle()

        # idle and attack
        if self.state is SproutState.idle:
            if next(self.look_timer):
                self.look_around()

                if self.enemies_in_sight:
                    self.target = self.get_nearest_enemy()

            if self.target:
                self.state = SproutState.attack
            else:
                self.go_idle()

        # seek pos
        if self.state is SproutState.seek_pos:
            if self.target.pos.distance_squared_to(self.pos) <= self.pos_range ** 2:
                self.sit_down()

    def stand_up(self):
        self.world.get_tile(self.pos).unblock(self)

        self.events.append({
            "name": "stand_up"
        })

    def sit_down(self):
        t = self.world.get_tile(self.pos)
        if not t.state:
            self.set_pos(self.target.pos)
            t.block(self)
            self.go_idle()

            self.events.append({
                "name": "sit_down"
            })
        else:
            self.go_wait(3)

    def go_idle(self):
        self.target = None
        self.state = SproutState.idle

    def go_wait(self, time=0):
        self.state = SproutState.wait
        self.wait_timer = time

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
        x, y = target

        x = int(x) + 0.5
        y = int(y) + 0.5

        self.target = TargetPosition(Vector2(x, y))
        self.state = SproutState.seek_pos
        self.stand_up()

    def kill(self):
        super().kill()
        self.stand_up()

class TargetPosition:
    def __init__(self, pos: Vector2):
        self.pos = pos


class SproutState(Enum):
    idle = 0
    seek_pos = 1
    attack = 2
    wait = 3
