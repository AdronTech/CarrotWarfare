from pygame import math


class Entity:

    def __init__(self):
        self.pos = math.Vector2()
        self.events = []

    def update(self):
        pass
