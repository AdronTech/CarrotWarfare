from rendering.abstract_renderer import *
from rendering.ultimate_version.screen_shake import *


class UltimateRenderer(AbstractRenderer):
    def __init__(self):
        load_all()
        self.main_surface = get_ultimate_surface()

        from rendering.ultimate_version.ground_layer import GroundLayer
        from rendering.ultimate_version.overlay_layer import OverlayLayer
        from rendering.ultimate_version.entity_layer import EntityLayer
        from rendering.ultimate_version.ui_layer import UILayer

        arena_subsurface = self.main_surface.subsurface(Rect(SUB_SURFACE_POSITION, SUB_SURFACE_SIZE))
        self.ground_layer = GroundLayer(self, arena_subsurface)
        self.overlay_layer = OverlayLayer(self, arena_subsurface)
        self.entity_layer = EntityLayer(self, arena_subsurface)

        ui_x_left = SCREEN_SHAKE_OFFSET[0]
        ui_x_right = SCREEN_SHAKE_OFFSET[0] + SUB_SURFACE_SIZE[0] + UI_SUBSURFACE_SIZE[0]
        ui_y_top = SCREEN_SHAKE_OFFSET[1]
        ui_y_bottom = SCREEN_SHAKE_OFFSET[1] + UI_SUBSURFACE_SIZE[1]

        player_ui_sub_surfaces = [
            self.main_surface.subsurface((SCREEN_SHAKE_OFFSET, UI_SUBSURFACE_SIZE)),
            self.main_surface.subsurface(((ui_x_right, ui_y_top), UI_SUBSURFACE_SIZE)),
            self.main_surface.subsurface(((ui_x_left, ui_y_bottom), UI_SUBSURFACE_SIZE)),
            self.main_surface.subsurface(((ui_x_right, ui_y_bottom), UI_SUBSURFACE_SIZE))]
        self.ui_layer = UILayer(self, player_ui_sub_surfaces)
        self.screen_shake = ScreenShaker()

    def render(self, target: Surface, world: World):
        for e in world.events:
            if e["name"] == "player_death":
                self.screen_shake.impulse(0.5)
        self.ground_layer.render(world)
        self.overlay_layer.render(world)
        self.entity_layer.render(world)
        self.ui_layer.render(world)
        # blit final image
        shake_off = self.screen_shake.get_shake()
        target.blit(self.main_surface, (0, 0), (shake_off, DISPLAY_RESOLUTION))
        world.events.clear()


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

    game_world = new_game()

    # main loop
    clock = Clock()
    pygame_init()
    display = PyGameWindow()
    from game.world import new_game

    DEFAULT_RENDERER = UltimateRenderer()
    DEFAULT_RENDERER.screen_shake.impulse(1)
    game_world = new_game()

    # main loop
    last_update = now()
    while True:

        # event
        for e in pygame_events.get():
            if e.type is QUIT:
                quit()
        pygame_events.pump()

        if now() >= last_update + update_delay:
            # update timing
            next(update_counter)
            last_update += update_delay
            game_world.update()
        else:
            # update timing
            next(redraw_counter)
            DEFAULT_RENDERER.render(display.render_target, game_world)
            display.flip()

            # DEFAULT_RENDERER.paint_square((randint(0, 19), randint(0, 19)), randint(0, 3))
            # 1DEFAULT_RENDERER.screen_shake_current = (random() * 2 - 1, random() * 2 - 1)
            DEFAULT_RENDERER.render(display.render_target, game_world)
