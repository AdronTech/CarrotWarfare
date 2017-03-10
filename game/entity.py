from game.world import *
from game.bounding_box import BoundingBox, collision


class Entity:
    def __init__(self, world, alliance, pos: Vector2 = Vector2(), hp=0):
        self.pos = pos

        self.events = []
        self.world = world
        self.render_flags = {}
        self.alliance = alliance
        self.dir = Vector2(1, 0)  # type: Vector2
        self.hp = hp
        self.death_stamp = None

        self.soft_lock = 0
        self.hard_lock = 0

        self.bb = BoundingBox(self.pos, Vector2(0.999, 0.999))

        self.register()

    def update(self, input=None):
        self.soft_lock -= delta_time
        self.hard_lock -= delta_time

    def set_pos(self, pos: Vector2):

        # unregister
        self.unregister()

        # Saman fix
        if pos.y < 0.5:
            self.pos = Vector2()+(pos[0], 0.5)
            self.bb.pos = Vector2()+(pos[0], 0.5)
        else:
            self.pos = pos
            self.bb.pos = pos

        # constrain
        self.world.constrain_vector(pos)

        if not self.death_stamp:
            # register
            self.register()

    def register(self):
        t = self.world.get_tile(self.pos)   # type: Tile
        t.register(self)

        for p in self.bb.get_int():
            t = self.world.get_tile(p)  # type: Tile
            if t:
                t.reg_coll(self)

    def unregister(self):
        t = self.world.get_tile(self.pos)  # type: Tile
        t.unregister(self)

        for p in self.bb.get_int():
            t = self.world.get_tile(p)  # type: Tile
            if t:
                t.unreg_coll(self)

    def hit(self, damage):
        self.hp -= damage

        self.events.append({
            "name": "hit",
            "damage": damage,
            "remaining": self.hp
        })

        if self.hp <= 0:
            self.hp = 0

            self.death_stamp = now()

            self.world.events.append({
                "name": "death",
                "stamp": self.death_stamp,
                "author": self
            })

    def kill(self):
        self.unregister()


