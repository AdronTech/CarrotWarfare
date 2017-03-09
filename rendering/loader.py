from pygame import Surface, error, image
from os.path import join
from rendering.constants import IMAGE_RESOURCE, TILE_SIZE
from pygame import transform
from pygame import PixelArray
from rendering.constants import REPLACEMENT_COLOR_LIGHT, REPLACEMENT_COLOR_DARK, COLOR_PLAYERS, COLOR_PLAYERS_DARK

RESOURCE_TILE_SIZE = 128


def load(path: str) -> Surface:
    try:
        img = image.load_extended(join('assets/sprites', path + ".png"))
    except error:
        raise SystemExit("Could not load image from {}".format(path))

    img.convert_alpha(img)
    return img


def put_values_for_entity(block: dict, name: str, alliance: int):
    resource = load(block[name + "_generic"]["name"])
    PixelArray(resource).replace(REPLACEMENT_COLOR_LIGHT, COLOR_PLAYERS[alliance], 0)
    PixelArray(resource).replace(REPLACEMENT_COLOR_DARK, COLOR_PLAYERS_DARK[alliance], 0)
    for x in range(4):
        for y in range(4):
            if x == 0 and y == 0:
                state = "state_stand"
            if y == 0:
                state = "state_walk"
            if y == 1:
                state = "state_attack"
            if y == 2:
                state = "state_growing"
            if y == 3:
                state = "state_die"

            if state == "state_stand":
                srf_size = (RESOURCE_TILE_SIZE, RESOURCE_TILE_SIZE)
                srf = Surface(srf_size)
                srf.blit(resource, (0, 0), ((RESOURCE_TILE_SIZE * x, RESOURCE_TILE_SIZE * y), srf_size))
                transform.scale(srf, (int(TILE_SIZE), int(TILE_SIZE)))

                block[name + str(alliance)][state]["frame" + str(x)] = srf
                block[name + str(alliance)]["state_walk"]["frame" + str(x)] = srf

                block[name + "_generic"]["offset"] = (int(TILE_SIZE / -2), -int(TILE_SIZE))
            else:
                srf_size = (RESOURCE_TILE_SIZE, RESOURCE_TILE_SIZE)
                srf = Surface(srf_size)
                srf.blit(resource, (0, 0), ((RESOURCE_TILE_SIZE * x, RESOURCE_TILE_SIZE * y), srf_size))
                transform.scale(srf, (int(TILE_SIZE), int(TILE_SIZE)))

                block[name + str(alliance)][state]["frame" + str(x)] = srf


def load_all():
    put_values_for_entity(IMAGE_RESOURCE["entities"], "player", 0)
    put_values_for_entity(IMAGE_RESOURCE["entities"], "player", 1)
    put_values_for_entity(IMAGE_RESOURCE["entities"], "player", 2)
    put_values_for_entity(IMAGE_RESOURCE["entities"], "player", 3)

    put_values_for_entity(IMAGE_RESOURCE["entities"], "carrot", 0)
    put_values_for_entity(IMAGE_RESOURCE["entities"], "carrot", 1)
    put_values_for_entity(IMAGE_RESOURCE["entities"], "carrot", 2)
    put_values_for_entity(IMAGE_RESOURCE["entities"], "carrot", 3)

    put_values_for_entity(IMAGE_RESOURCE["entities"], "sprout", 0)
    put_values_for_entity(IMAGE_RESOURCE["entities"], "sprout", 1)
    put_values_for_entity(IMAGE_RESOURCE["entities"], "sprout", 2)
    put_values_for_entity(IMAGE_RESOURCE["entities"], "sprout", 3)
