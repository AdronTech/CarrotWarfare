from game.world import *


class Entity:
    def __init__(self, world, alliance, pos: Vector2 = Vector2(), hp=0):
        self.pos = pos

        self.events = []
        self.world = world
        self.render_flags = {}
        self.alliance = alliance
        self.dir = Vector2(1, 0)
        self.hp = hp
        self.death_stamp = None

        self.soft_lock = 0
        self.hard_lock = 0

        self.register()

    def update(self, input=None):
        self.soft_lock -= delta_time
        self.hard_lock -= delta_time

    def set_pos(self, pos: Vector2):

        # unregister
        self.unregister()

        self.pos = pos

        # constrain
        self.world.constrain_vector(pos)

        # register
        self.register()

    def register(self):
        t = self.world.get_tile(self.pos)   # type: Tile
        t.register(self)

    def unregister(self):
        t = self.world.get_tile(self.pos)  # type: Tile
        t.unregister(self)

    def hit(self, damage):
        self.hp -= damage

        self.events.append({
            "name": "hit",
            "damage": damage,
            "remaining": self.hp
        })

        if self.hp < 0:
            self.hp = 0
            self.death()

            self.unregister()
            self.death_stamp = now()

            self.events.append({
                "name": "death",
                "stamp": self.death_stamp
            })

    def death(self):
        pass


