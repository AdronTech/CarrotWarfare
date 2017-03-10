# system imports
from asyncio import get_event_loop
from enum import Enum
# pygame imports
from pygame import event as pygame_events
from pygame import init as pygame_init
from display import *
# own imports

if True:
    from rendering.ultimate_version.renderer import UltimateRenderer as Renderer
else:
    from rendering.simple_renderer import SimpleRenderer as Renderer

from rendering import debugger as Debug
from game.world import new_game
from timing import *
from game.input import get_input


class ExitCode(Enum):
    EXIT = 0
    PAUSE = 1


class Application:
    def __init__(self):
        pygame_init()
        self.display = PyGameWindow()
        self.started = False
        self.running = False
        self.game = None
        self.loop = get_event_loop()

    async def process_start(self):
        self.started = True
        self.running = True
        await self._main_menu()
        print("done")

    async def _main_menu(self):
        while self.running:
            self.game = {"world": new_game(), "renderer": Renderer()}
            # run the process
            exit_code = self._game_loop(**self.game)
            # handle exit
            if exit_code is ExitCode.EXIT:
                self.game = None
                self.running = False
            elif exit_code is ExitCode.PAUSE:
                pass

    def _game_loop(self, world, renderer):
        # basic loop fuctions
        game_render = renderer.render
        game_update = world.update

        # start of main loop
        last_update = now()
        while True:
            time_since_update = now() - last_update

            events = pygame_events.get()
            # event handling
            for e in events:
                if e.type is QUIT or (e.type is KEYDOWN and e.key is K_ESCAPE):
                    return ExitCode.EXIT

            input = get_input(events, renderer, world)
            pygame_events.pump()

            if time_since_update >= update_delay:
                Debug.clear()
                game_update(input)
                for e in world.events:
                    if e["name"] is "main_menu":
                        return ExitCode.PAUSE

                # update timing
                next(update_counter)
                last_update += update_delay
            else:
                game_render(self.display.render_target, world)
                self.display.flip()

                # update timing
                next(redraw_counter)
                # update or render



if __name__ == "__main__":
    app = Application()
    app.loop.run_until_complete(app.process_start())
