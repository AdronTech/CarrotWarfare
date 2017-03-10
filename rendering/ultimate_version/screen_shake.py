from timing import now
from pygame.math import Vector2
from rendering.constants import *
from math import sin, cos
from random import random

PI = 3.1
DAMP_PERCENT = 0.25
NOISE_PERCENT = 0.4
SPEED = (Vector2()+SCREEN_SHAKE_OFFSET).length()**2


class ScreenShaker:
    def __init__(self):
        self.strength = 0
        self.shake = None

    def impulse(self, impulse: float):
        if impulse > self.strength:
            self.strength = impulse
            self.shake = self.shake_generator()

    def get_shake(self):
        if self.shake:
            x, y = next(self.shake)
            return x, y
        else:
            return 0, 0

    def shake_generator(self):
        last_update = now()
        angle = PI * 2 * random()
        pos_last = Vector2()
        pos_next = Vector2() + (cos(angle), sin(angle))
        travel_progress = 0
        move_distance = (pos_next-pos_last).length()
        while self.strength > 0.001:
            dt = (now() - last_update)/1000
            if travel_progress < 1:
                travel_progress += dt/move_distance * SPEED
                shake = (pos_next - pos_last) * min(1, travel_progress)
            else:
                travel_progress = 0
                pos_last = pos_next
                noise = angle * NOISE_PERCENT
                noise -= 2 * random() * noise
                angle += PI + noise
                self.strength *= 1 - DAMP_PERCENT
                diretion = Vector2() + (cos(angle), sin(angle))
                pos_next = diretion * self.strength
                move_distance = (pos_next - pos_last).length()
                shake = pos_last
            last_update = now()
            yield shake
        self.shake = None
        yield 0, 0

if __name__ == "__main__":
    from pygame.time import Clock
    clock = Clock()
    shake = ScreenShaker()
    shake.impulse(1)
    while shake.strength > 0:
        print("{0}{1.pos_current}{1.hold}".format(shake.get_shake(), shake))
        clock.tick(60)