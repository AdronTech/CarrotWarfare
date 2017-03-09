from rendering.ultimate_version.renderer import *


class Pop(object):
    def __init__(self, srf: Surface, buffer: Surface, target: Surface, pos: (int, int)):
        buffer.blit(srf, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))
        self.target = target
        self.updated = now()
        self.pos = pos
        self.buffer = buffer

    def pop(self):
        position = (self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE)
        self.target.blit(self.buffer, (0, 0), (position, (TILE_SIZE, TILE_SIZE)))


class GroundLayer:
    def __init__(self, renderer: UltimateRenderer, arena_subsurface: Surface):
        self.parent_renderer = renderer  # type: UltimateRenderer
        self.ground_surface = Surface(ARENA_SURFACE_SIZE)
        self.buffer_surface = Surface(ARENA_SURFACE_SIZE)
        self.ground_surface.fill(COLOR_BACKGROUND)
        self.arena_subsurface = arena_subsurface
        self.buffer = []

    def buffer_contains(self, tile: Tile):
        for e in self.buffer:  # type: Pop
            if e.pos[0] == tile.x and e.pos[1] == tile.y:
                return True
        return False

    def splatter(self, entity: Entity, pos: (int, int)):

        count = 3
        for i in range(count):
            if issubclass(type(entity), Bullet):
                radius = int(random() * TILE_SIZE)
            else:
                radius = int(random() * TILE_SIZE + TILE_SIZE / 2)
            x = int((pos[0] + random() * 2) * TILE_SIZE)
            y = int((pos[1] + random() * 2) * TILE_SIZE)
            aacircle(self.ground_surface, x, y, radius, COLOR_PLAYERS_LIGHT[entity.alliance])
            filled_circle(self.ground_surface, x, y, radius, COLOR_PLAYERS_LIGHT[entity.alliance])
            aacircle(self.buffer_surface, x, y, radius, COLOR_PLAYERS_LIGHT[entity.alliance])
            filled_circle(self.buffer_surface, x, y, radius, COLOR_PLAYERS_LIGHT[entity.alliance])

    def render(self, world: World):
        for e in world.events:
            if not "rendered" in e:
                if e["name"] == "death":
                    self.parent_renderer.ground_layer.splatter(e["author"], e["author"].pos)
                if e["name"] == "plant_request":
                    if "allowed" in e:
                        if not self.buffer_contains(e["tile"]):
                            srf = Surface((TILE_SIZE, TILE_SIZE))
                            target_rect = ((e["tile"].x * TILE_SIZE, e["tile"].y * TILE_SIZE),
                                           (TILE_SIZE, TILE_SIZE))
                            srf.blit(self.ground_surface, (0, 0), target_rect)

                            self.buffer.append(Pop(srf, self.buffer_surface,
                                                   self.ground_surface.subsurface(target_rect),
                                                   (e["tile"].x, e["tile"].y)))

                            self.ground_surface.fill(COLOR_BACKGROUND_SECONDARY, target_rect)

                elif e["name"] == "full_grown":
                    for i in range(len(self.buffer)):
                        if self.buffer[i].pos == (e["tile"].x, e["tile"].y):
                            self.buffer[i].pop()
                            del self.buffer[i]
                            break

                e["rendered"] = True

        self.arena_subsurface.blit(self.ground_surface, (0, 0))
