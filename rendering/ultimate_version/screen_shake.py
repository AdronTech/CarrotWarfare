from timing import now
from pygame.math import Vector2
from rendering.constants import *
from math import sin, cos
from random import random

PI = 3.1
DAMP_PERCENT = 0.1
NOISE_PERCENT = 0.4
SPEED = 100


class ScreenShaker:
    def __init__(self):
        # new pos calculation
        self.hold = True
        self.remaining_force = 0
        self.angle = PI * 2 * random()
        # screen position
        self.pos_next = Vector2()
        self.pos_current = Vector2()
        # timing
        self.last_update = now()

    def impulse(self, impulse: float):
        if self.hold:
            self.hold = False
            self.remaining_force = impulse
        elif impulse > self.remaining_force:
            self.remaining_force = impulse

    def set_next_position(self):
        if self.remaining_force < 0.0001:
            self.remaining_force = 0
            hold = True
            return
        noise = self.angle * NOISE_PERCENT
        noise -= 2 * random() * noise

        self.angle += PI + noise
        self.remaining_force *= 1 - DAMP_PERCENT
        diretion = Vector2()+(cos(self.angle), sin(self.angle))
        self.pos_next = diretion * self.remaining_force

    def get_shake(self):
        if self.remaining_force == 0:
            return SCREEN_SHAKE_OFFSET
        else:
            dt = (now() - self.last_update)/1000
            delta = (self.pos_next - self.pos_current)
            if delta.length() <= 0.01:
                self.set_next_position()
            self.pos_current += delta * SPEED * dt
            x = SCREEN_SHAKE_OFFSET[0] * (1 + self.pos_current.x)
            y = SCREEN_SHAKE_OFFSET[1] * (1 + self.pos_current.y)
            self.last_update = now()
            return x, y

if __name__ == "__main__":
    from pygame.time import Clock
    clock = Clock()
    shake = ScreenShaker()
    shake.impulse(1)
    while shake.remaining_force > 0:
        print("{0}{1.pos_current}{1.hold}".format(shake.get_shake(), shake))
        clock.tick(60)