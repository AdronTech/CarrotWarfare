from game.entity import *


class Bullet(Entity):
    def __init__(self, world: World, alliance, pos: Vector2, dir: Vector2):
        super().__init__(world, alliance, pos, 10000)

        self.speed = 3
        self.dir = Vector2() + dir

        self.attack_range = 1
        self.damage = 2

        self.bb.dim = Vector2(0.5, 0.5)

    def update(self, input=None):

        self.set_pos(self.pos + self.dir * self.speed * delta_time)

        for p in self.bb.get_int():
            t = self.world.get_tile(p)  # type: Tile

            if t:
                if t.collider:
                    for ent in t.collider:  # type: Entity
                        if ent is self:
                            continue

                        if ent.alliance is self.alliance:
                            continue

                        if collision(ent.bb, self.bb):
                            self.collided()
            else:
                self.collided()

    def collided(self):
        self.hit(10000)
        self.world.events.append({
            "name": "attack",
            "pos": self.pos,
            "dir": self.dir,
            "range": self.attack_range,
            "angle": 360,
            "alliance": self.alliance,
            "damage": self.damage,
            "count": 2,
            "author": self
        })

        # Debug.circle(Color("black"), self.pos, 0.25)
