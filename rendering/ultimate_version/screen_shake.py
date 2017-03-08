from timing import now
from pygame.math import Vector2
from rendering.constants import *
from math import pi, sin, cos
from random import random

DAMP_PERCENT = 0.2
NOISE_PERCENT = 0.2


class ScreenShaker:
    def __init__(self):
        # new pos calculation
        self.remaining_force = 0
        self.angle = 0
        # screen position
        self.pos = 1
        self.pos_last = Vector2()
        self.pos_next = Vector2()
        self.pos_current = Vector2()
        # timing
        self.last_update = now()

    def impulse(self, impulse: float):
        if impulse > self.remaining_force:
            self.remaining_force = impulse
            self.angle = pi * 2 * random()

    def set_next_position(self):
        self.pos_last = self.pos_next
        noise = self.angle * NOISE_PERCENT
        noise -= 2 * noise * random()

        self.angle += pi + noise
        # set new direction
        self.pos_next.x = cos(self.angle)
        self.pos_next.y = sin(self.angle)
        # deminish the force
        self.remaining_force *= 1 - DAMP_PERCENT
        if self.remaining_force < 0.01:
            self.remaining_force = 0
        # scale position by remaining force
        self.pos_next *= self.remaining_force

    def get_shake(self):
        # move between shake points
        if self.pos < 1:
            self.pos += (now() - self.last_update)/1000
        else:
            self.set_next_position()

        if self.remaining_force > 0:
            self.pos_current = position = self.pos_last + (self.pos_next - self.pos_last) * self.pos
            x = SCREEN_SHAKE_OFFSET[0] * (1 + self.pos_current.x)
            y = SCREEN_SHAKE_OFFSET[1] * (1 + self.pos_current.y)
        else:
            x = SCREEN_SHAKE_OFFSET[0]
            y = SCREEN_SHAKE_OFFSET[1]
        self.last_update = now()
        return x, y

if __name__ == "__main__":
    from pygame.time import Clock
    clock = Clock()
    shake = ScreenShaker()
    shake.impulse(1)
    while shake.remaining_force > 0:
        print(str(shake.get_shake()))
        clock.tick(10)