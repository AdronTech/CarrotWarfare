from pygame.math import Vector2
from math import floor


class BoundingBox:
    def __init__(self, pos: Vector2, dim: Vector2):
        self.pos = pos
        self.dim = dim

    def top(self):
        return self.pos.y - self.dim.y / 2

    def right(self):
        return self.pos.x + self.dim.x / 2

    def bottom(self):
        return self.pos.y + self.dim.y / 2

    def left(self):
        return self.pos.x - self.dim.x / 2

    def get_int(self):
        for x in range(floor(self.left()), floor(self.right()) + 1):
            for y in range(floor(self.top()), floor(self.bottom()) + 1):
                yield Vector2(x, y)


def collision(bb1: BoundingBox, bb2: BoundingBox) -> bool:
    return not (bb1.top() > bb2.bottom() or
                bb1.right() < bb2.left() or
                bb1.bottom() < bb2.top() or
                bb1.left() > bb2.right())
