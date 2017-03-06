from pygame import init as pygame_init
from timing import update_counter, redraw_counter, update_delay, now
from display import PyGameWindow


if __name__ == "__main__":
    pygame_init()
    display = PyGameWindow()
    from rendering.renderer import TestRenderer as Renderer
    DEFAULT_RENDERER = Renderer()
    from game.world import World
    game_world = World()

    # main loop
    next_update = now()
    while True:
        if next_update == now():
            # update timing
            next(update_counter)
            next_update += update_delay
            game_world.update()
        else:
            # update timing
            next(redraw_counter)
            DEFAULT_RENDERER.render(display.render_target, game_world)
            display.flip()