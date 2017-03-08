from rendering.ultimate_version.renderer import *


class Pop(object):
    def __init__(self, srf: Surface, target: Surface, pos: (int, int)):
        self.surface = srf
        self.target = target
        self.updated = now()
        self.pos = pos

    def pop(self):
        self.target.blit(self.surface, (0, 0))


class GroundLayer:
    def __init__(self, renderer: UltimateRenderer, arena_subsurface: Surface):
        self.parent_renderer = renderer  # type: UltimateRenderer
        self.ground_surface = Surface(SUB_SURFACE_SIZE)
        self.ground_surface.fill(COLOR_BACKGROUND)
        self.arena_subsurface = arena_subsurface
        self.buffer = []

    def buffer_contains(self, pos: (int, int)):
        for e in self.buffer:  # type: Pop
            if e.pos == pos:
                return True
        return False

    def render(self, world: World):
        for e in world.events:
            if e["name"] == "plant":
                if not self.buffer_contains(e["pos"]):
                    srf = Surface((TILE_SIZE, TILE_SIZE))
                    target_rect = ((e["pos"]["x"] * TILE_SIZE, e["pos"]["y"] * TILE_SIZE),
                                   (TILE_SIZE, TILE_SIZE))
                    srf.blit(self.ground_surface, (0, 0), target_rect)

                    self.ground_surface.fill(COLOR_BACKGROUND_SECONDARY, target_rect)

                    self.buffer.append(Pop(srf, self.ground_surface.subsurface(target_rect), e["pos"]))

            elif e["name"] == "full_grown":
                for i in range(len(self.buffer)):
                    if (int(self.buffer[i].pos["x"]),
                        int(self.buffer[i].pos["y"])) == (int(e["pos"][0]),
                                                          int(e["pos"][1])):
                        self.buffer[i].pop()
                        del self.buffer[i]

        self.arena_subsurface.blit(self.ground_surface, (0, 0))
