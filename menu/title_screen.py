from pygame.font import Font
from pygame import Surface
from rendering.constants import *
from enum import Enum
from pygame import time
from pygame.event import get, pump
from pygame.locals import *
from timing import now
from math import pi, sin
from game.input import poll_connections
from pygame import display

TITLE_TXT = "CARROT WARFARE"
FADE_IN_TIME = 2
WAVE_TIME = 2
PLAYER_FADE_IN = 0.5

class TitleAnimationStates(Enum):
    fade_in = 0
    idle = 1


def poll_for_players(render_target: Surface):
    cycle_start = now() + FADE_IN_TIME * 1000
    title_font = Font("assets/fonts/RobotoMono-Regular.ttf", 90)
    title = title_font.render(TITLE_TXT, 1, (0, 0, 0))
    title_x = (render_target.get_size()[0] - title.get_size()[0])/2
    title_y = (render_target.get_size()[1] - title.get_size()[1])/2
    start_y = RENDER_RESOLUTION[1]*0.25
    wave_delta = RENDER_RESOLUTION[1]*0.03

    size = render_target.get_size()
    middle = size[0]/2
    connect_sign_size = (size[0]*0.1, size[1]*0.1)
    connect_sign_origin_y = size[1]*0.80
    done = False
    show = [0] * 4
    time = [None] * 4
    while not done:
        # event handling
        for e in get():
            if e.type is QUIT or (e.type is KEYDOWN and e.key is K_ESCAPE):
                quit()
            elif e.type is KEYDOWN and e.key is K_SPACE:
                done = True
        pump()
        render_target.fill((255, 255, 255))

        if now() < cycle_start:
            factor = (cycle_start - now()) / FADE_IN_TIME / 1000
            cur_y = start_y + (title_y - start_y) * (1-factor)
            title = title_font.render(TITLE_TXT, 1, (255*factor, 255*factor, 255*factor))
            render_target.blit(title, (title_x, cur_y))
        else:
            factor = (cycle_start - now()) / FADE_IN_TIME / 1000
            render_target.blit(title, (title_x, cur_y-wave_delta*sin(pi * factor/WAVE_TIME)))

            tmp = poll_connections()
            for i in range(len(tmp)):
                if tmp[i]:
                    if not time[i]:
                        time[i] = now()
                        # TODO insert audio YEAH on connection
                    show[i] = min(1, (now() - time[i]) / (FADE_IN_TIME * 1000))
                else:
                    if time[i]:
                        time[i] = None
                        show[i] = 0

                x = middle + connect_sign_size[0] * (i - 2)
                y = connect_sign_origin_y
                r = 255 + (COLOR_PLAYERS[i][0] - 255) * show[i]
                g = 255 + (COLOR_PLAYERS[i][1] - 255) * show[i]
                b = 255 + (COLOR_PLAYERS[i][2] - 255) * show[i]
                render_target.fill((r, g, b),
                                   ((x, y), connect_sign_size))

        display.flip()
    from game.world import new_game
    return new_game()