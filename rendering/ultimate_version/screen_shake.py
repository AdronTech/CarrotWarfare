class ScreenShaker:
    def __init__(self, offset):
        self.rest_force = 0
        self.shake_offset = offset
        self.screen_shake_current = [0, 0]

    def impulse(self, i: float):
        if i > self.rest_force:
            self.rest_force = i

    def get_shake(self):
        x = self.shake_offset * (1 + self.screen_shake_current[0])
        y = self.shake_offset * (1 + self.screen_shake_current[1])
        return x, y