from rendering.abstract_renderer import *
from rendering.ultimate_version.screen_shake import *
from rendering import debugger as Debug


class UltimateRenderer(AbstractRenderer):
    def __init__(self):
        super().__init__()

        load_all()

        self.buffer_surface = Surface(RENDER_RESOLUTION)
        self.arena_surface = Surface(ARENA_SURFACE_SIZE)

        Debug.gen_debug_surface(self.arena_surface)

        from rendering.ultimate_version.ui_layer import UILayer
        from rendering.ultimate_version.ground_layer import GroundLayer
        from rendering.ultimate_version.overlay_layer import OverlayLayer
        from rendering.ultimate_version.entity_layer import EntityLayer

        self.ui_layer = UILayer(self, self.buffer_surface)
        self.ground_layer = GroundLayer(self, self.arena_surface)
        self.overlay_layer = OverlayLayer(self, self.arena_surface)
        self.entity_layer = EntityLayer(self, self.arena_surface)

        self.screen_shake = ScreenShaker()

    def render(self, target: Surface, world: World):
        for e in world.events:
            if e["name"] == "death" and type(e["author"]) is Player:
                self.screen_shake.impulse(0.5)
        self.ui_layer.render(world)
        self.ground_layer.render(world)
        self.overlay_layer.render(world)
        self.entity_layer.render(world)

        # markus debuggger
        Debug.render(self.arena_surface)

        # blit arena to main surface
        x, y = ARENA_SURFACE_PADDING
        s_dx, s_dy = self.screen_shake.get_shake()

        self.arena_surface_offset = (x+s_dx, y+s_dy)

        self.buffer_surface.blit(self.arena_surface, self.arena_surface_offset)

        # remove all recent events
        world.events.clear()

        # blit final image
        target.blit(self.buffer_surface, (0, 0))


if __name__ == "__main__":
    from pygame import event as pygame_events
    from pygame.time import Clock
    from timing import redraw_counter
    from pygame.locals import *
    from game.world import new_game
    from pygame import init as pygame_init
    from pygame import event as pygame_events
    from display import PyGameWindow
    from timing import *
    from random import random, randint

    # main loop
    clock = Clock()
    pygame_init()
    display = PyGameWindow()

    DEFAULT_RENDERER = UltimateRenderer()
    DEFAULT_RENDERER.screen_shake.impulse(1)
    game_world = new_game()
    Debug.gen_debug_surface(DEFAULT_RENDERER.arena_surface)
    # main loop
    last_update = now()
    while True:

        # event
        for e in pygame_events.get(QUIT):
            if e.type is QUIT:
                quit()
        pygame_events.pump()

        if now() >= last_update + update_delay:
            # update timing
            next(update_counter)
            last_update += update_delay
            Debug.clear()
            game_world.update()
        else:
            # update timing
            next(redraw_counter)
            DEFAULT_RENDERER.render(display.render_target, game_world)
            display.flip()
