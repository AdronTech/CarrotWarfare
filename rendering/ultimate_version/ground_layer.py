from rendering.ultimate_version.renderer import *

FRAME_DURATION = 1000


class Pop:
    def __init__(self, srf: Surface, buffer: Surface, target: Surface, pos: (int, int)):
        buffer.blit(srf, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))
        self.target = target
        self.pos = (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)
        self.buffer = buffer

    def pop(self):
        self.target.blit(self.buffer, (0, 0), (self.pos, (TILE_SIZE, TILE_SIZE)))


class Animator:
    def __init__(self, name: str, target: Surface, pos: (int, int)):
        self.target = target
        self.updated = 0
        self.pos = pos
        self.block = IMAGE_RESOURCE["entities"][name]
        self.last_frame = -1

    def update(self):
        if (now() - self.updated) > FRAME_DURATION:
            frame = self.last_frame + 1
            self.updated = now()
        else:
            return False, False
        if frame == 4:
            return True, False

        self.last_frame = frame
        return False, True

    def render(self):
        pos = self.pos
        srf = self.block["state_growing"]["right"]["frame" + str(self.last_frame)]
        self.target.blit(srf, pos)


class GroundLayer:
    def __init__(self, renderer: UltimateRenderer, arena_subsurface: Surface):
        self.parent_renderer = renderer  # type: UltimateRenderer
        self.ground_surface = Surface(ARENA_SURFACE_SIZE)
        self.buffer_surface = Surface(ARENA_SURFACE_SIZE)
        self.ground_surface.fill(COLOR_BACKGROUND)
        self.arena_subsurface = arena_subsurface
        self.buffer = []
        self.animators = []

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

        for i in range(len(self.animators)):
            fin, redraw = self.animators[i].update()
            if redraw:
                for p in self.buffer:  # type: Pop
                    if p.pos == self.animators[i].pos:
                        p.pop()
                self.animators[i].render()
            if fin:
                for p in self.buffer:  # type: Pop
                    if p.pos == self.animators[i].pos:
                        p.pop()
                del self.animators[i]
                break

        for e in world.events:
            if "rendered" not in e:

                if e["name"] == "death":
                    self.parent_renderer.ground_layer.splatter(e["author"], e["author"].pos)
                    if type(e["author"]) is Player:
                        self.parent_renderer.screen_shake.impulse(50)

                elif e["name"] == "plant_request":
                    if "allowed" in e:
                        if not self.buffer_contains(e["tile"]):
                            srf = Surface((TILE_SIZE, TILE_SIZE))
                            target_rect = ((e["tile"].x * TILE_SIZE, e["tile"].y * TILE_SIZE),
                                           (TILE_SIZE, TILE_SIZE))
                            srf.blit(self.ground_surface, (0, 0), target_rect)

                            self.buffer.append(Pop(srf, self.buffer_surface,
                                                   self.ground_surface.subsurface(target_rect),
                                                   (e["tile"].x, e["tile"].y)))

                            if e["type"] == SeedType.melee:
                                name = "carrot" + str(e["alliance"])
                            else:
                                name = "sprout" + str(e["alliance"])

                            anim = Animator(name, self.ground_surface, target_rect[0])
                            anim.update()
                            anim.render()
                            self.animators.append(anim)

                elif e["name"] == "full_grown":
                    for i in range(len(self.buffer)):
                        if self.buffer[i].pos == (e["tile"].x, e["tile"].y):
                            self.buffer[i].pop()
                            del self.buffer[i]
                            break

                elif e["name"] == "pick_up":
                    tile = e["tile"]  # type: Tile
                    del tile.render_flags["environment"]

                elif e["name"] == "pick_up_spawn":
                    tile = e["tile"]  # type: Tile
                    if e["type"] == SeedType.melee:
                        name = "melee"
                    else:
                        name = "ranged"
                    tile.render_flags["environment"] = IMAGE_RESOURCE["ui"][name]["resource"]

                e["rendered"] = True

        self.arena_subsurface.blit(self.ground_surface, (0, 0))
