from pygame import math


def do_nothing():
    pass


class Entity:
    def __init__(self):
        self.type = ""
        self.pos = math.Vector2()
        self.events = []
        self.dump = {}
        self.update = do_nothing
