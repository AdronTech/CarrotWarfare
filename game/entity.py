from pygame import math


def do_nothing(self):
    print(self.dump)
    pass


class Entity:
    def __init__(self):
        self.type = ""
        self.pos = math.Vector2()
        self.events = []
        self.dump = {}
        self.update_function = do_nothing

    def update(self):
        self.update_function(self)
