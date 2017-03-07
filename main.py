from pygame import init as pygame_init
from pygame import event as pygame_events
from timing import *
from display import PyGameWindow
from pygame.locals import *

if __name__ == "__main__":
    pygame_init()
    display = PyGameWindow()
    from rendering.debug import DebugRenderer as Renderer
    DEFAULT_RENDERER = Renderer()
    from game.world import new_game
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
