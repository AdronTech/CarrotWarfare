from pygame import Surface, draw, BLEND_RGBA_ADD, SRCALPHA
from rendering.constants import *

debug_surface = None  # type: Surface
debug = True


def gen_debug_surface(ref: Surface):
    global debug_surface
    debug_surface = Surface((ref.get_width(), ref.get_height()), SRCALPHA)
    clear()


def clear():
    debug_surface.fill((0, 0, 0, 0))


def render(surf: Surface):
    if debug:
        surf.blit(debug_surface, (0, 0))


def circle(color, pos, radius, width=0):
    x, y = pos

    x = int(x * TILE_SIZE)
    y = int(y * TILE_SIZE)

    radius = int(radius * TILE_SIZE)

    draw.circle(debug_surface, color, (x, y), radius, width)


def rect(color, rect, width=0):
    pos, dim = rect

    x, y = pos
    w, h = dim

    x = int(x * TILE_SIZE)
    y = int(y * TILE_SIZE)

    w = int(w * TILE_SIZE)
    h = int(h * TILE_SIZE)

    draw.rect(debug_surface, color, ((x, y), (w, h)), width)


def polygon(color, pointlist, width=0):
    mylist = []

    for p in pointlist:
        x, y = p

        x = int(x * TILE_SIZE)
        y = int(y * TILE_SIZE)

        mylist.append((x, y))

    draw.polygon(debug_surface, color, mylist, width)


def ellipse(color, rect, width=0):
    pos, dim = rect

    x, y = pos
    w, h = dim

    x = int(x * TILE_SIZE)
    y = int(y * TILE_SIZE)

    w = int(w * TILE_SIZE)
    h = int(h * TILE_SIZE)

    draw.ellipse(debug_surface, color, ((x, y), (w, h)), width)


def arc(color, rect, start_angle, stop_angle, width=1):
    pos, dim = rect

    x, y = pos
    w, h = dim

    x = int(x * TILE_SIZE)
    y = int(y * TILE_SIZE)

    w = int(w * TILE_SIZE)
    h = int(h * TILE_SIZE)

    draw.arc(color, (x, y), (w, h), start_angle, stop_angle, width)


def line(color, start_pos, end_pos, width=1):
    x1, y1 = start_pos
    x2, y2 = end_pos

    x1 = int(x1 * TILE_SIZE)
    y1 = int(y1 * TILE_SIZE)
    x2 = int(x2 * TILE_SIZE)
    y2 = int(y2 * TILE_SIZE)

    draw.line(debug_surface, color, (x1, y1), (x2, y2), width)


def lines(color, closed, pointlist, width=1):
    mylist = []

    for p in pointlist:
        x, y = p

        x = int(x * TILE_SIZE)
        y = int(y * TILE_SIZE)

        mylist.append((x, y))

    draw.lines(debug_surface, color, closed, mylist, width)


def aaline(color, startpos, endpos, blend=1):
    x1, y1 = startpos
    x2, y2 = endpos

    x1 = int(x1 * TILE_SIZE)
    y1 = int(y1 * TILE_SIZE)
    x2 = int(x2 * TILE_SIZE)
    y2 = int(y2 * TILE_SIZE)

    draw.aaline(debug_surface, color, (x1, y1), (x2, y2), blend)


def aalines(color, closed, pointlist, blend=1):
    mylist = []

    for p in pointlist:
        x, y = p

        x = int(x * TILE_SIZE)
        y = int(y * TILE_SIZE)

        mylist.append((x, y))

    draw.aaline(debug_surface, color, closed, mylist, blend)
