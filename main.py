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
    from rendering.simple_version.renderer import SimpleRenderer as Renderer

from sound.loader import Sound
from rendering import debugger as Debug
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
            from menu.title_screen import poll_for_players
            g = poll_for_players(self.display.render_target)
            self.game = {
                "world": g,
                "renderer": Renderer(self.display.native_resolution),
                "sound": Sound()
            }
            # run the process
            exit_code = self._game_loop(**self.game)
            # handle exit
            if exit_code is ExitCode.EXIT:
                self.game = None
                self.running = False
            elif exit_code is ExitCode.PAUSE:
                pass

    def _game_loop(self, world, renderer, sound):
        # basic loop fuctions
        game_render = renderer.render
        game_update = world.update
        game_sound = sound.update
        renderer.screen_shake.impulse(20)
        # start of main loop
        last_update = now()
        while True:
            time_since_update = now() - last_update

            events = pygame_events.get()
            # event handling
            for e in events:
                if e.type is QUIT or (e.type is KEYDOWN and e.key is K_ESCAPE):
                    return ExitCode.EXIT
                if e.type is KEYDOWN and e.key is K_TAB:
                    return ExitCode.PAUSE

            pygame_events.pump()

            if time_since_update >= update_delay:
                Debug.clear()
                input = get_input(events, world, renderer)
                game_update(input)
                game_sound(world)

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
