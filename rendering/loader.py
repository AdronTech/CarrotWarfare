from pygame import Surface, error, image, SRCALPHA
from os.path import join
from rendering.constants import IMAGE_RESOURCE, TILE_SIZE, ARENA_SURFACE_PADDING
from pygame import transform
from pygame import PixelArray
from rendering.constants import REPLACEMENT_COLOR_LIGHT, REPLACEMENT_COLOR_DARK, COLOR_PLAYERS, COLOR_PLAYERS_DARK

RESOURCE_TILE_SIZE = 128


def load(path: str) -> Surface:
    try:
        img = image.load_extended(join('assets/sprites', path + ".png"))
    except error:
        raise SystemExit("Could not load image from {}".format(path))

    return img


def put_values_for_entity(block: dict, name: str, alliance: int):
    resource = load(block[name + "_generic"]["name"])
    PixelArray(resource).replace(REPLACEMENT_COLOR_LIGHT, COLOR_PLAYERS[alliance], 0)
    PixelArray(resource).replace(REPLACEMENT_COLOR_DARK, COLOR_PLAYERS_DARK[alliance], 0)
    for x in range(4):
        for y in range(4):
            if x == 3 and y == 1:
                state = "state_stand"
            elif y == 0:
                state = "state_walk"
            elif y == 1:
                state = "state_attack"
            elif y == 2:
                state = "state_growing"
            elif y == 3:
                state = "state_die"

            if state == "state_stand":
                source_size = (RESOURCE_TILE_SIZE, RESOURCE_TILE_SIZE)
                srf_size = (TILE_SIZE, TILE_SIZE)
                source = Surface(source_size, SRCALPHA)
                srf = Surface(srf_size, SRCALPHA)
                source.blit(resource, (0, 0), ((RESOURCE_TILE_SIZE * x, RESOURCE_TILE_SIZE * y), source_size))
                transform.scale(source, (TILE_SIZE, TILE_SIZE), srf)

                block[name + str(alliance)][state]["left"]["frame0"] = srf
                block[name + str(alliance)]["state_attack"]["left"]["frame" + str(x)] = srf

                srf = transform.flip(srf, True, False)
                block[name + str(alliance)][state]["right"]["frame0"] = srf
                block[name + str(alliance)]["state_attack"]["right"]["frame" + str(x)] = srf

                block[name + "_generic"]["offset"] = (TILE_SIZE / -2, -TILE_SIZE)
            else:
                source_size = (RESOURCE_TILE_SIZE, RESOURCE_TILE_SIZE)
                srf_size = (TILE_SIZE, TILE_SIZE)
                source = Surface(source_size, SRCALPHA)
                srf = Surface(srf_size, SRCALPHA)
                source.blit(resource, (0, 0), ((RESOURCE_TILE_SIZE * x, RESOURCE_TILE_SIZE * y), source_size))
                transform.scale(source, (TILE_SIZE, TILE_SIZE), srf)

                block[name + str(alliance)][state]["left"]["frame" + str(x)] = srf

                srf = transform.flip(srf, True, False)
                block[name + str(alliance)][state]["right"]["frame" + str(x)] = srf


def load_pea(block: dict, alliance: int):
    resource = load(block["pea_generic"]["name"])
    srf = Surface((TILE_SIZE / 2, TILE_SIZE / 2), SRCALPHA)
    transform.scale(resource, (TILE_SIZE // 2, TILE_SIZE // 2), srf)
    PixelArray(srf).replace(REPLACEMENT_COLOR_LIGHT, COLOR_PLAYERS[alliance], 0)
    PixelArray(srf).replace(REPLACEMENT_COLOR_DARK, COLOR_PLAYERS_DARK[alliance], 0)

    block["pea" + str(alliance)]["resource"] = srf

    block["pea_generic"]["offset"] = (TILE_SIZE / -2 + TILE_SIZE / 4, -TILE_SIZE)


def load_ui(block: dict):
    img = load("carrotUI")
    img = img.convert_alpha(img)
    size = int(ARENA_SURFACE_PADDING[0]/3), int(ARENA_SURFACE_PADDING[0]/3)
    srf = Surface(size, SRCALPHA)
    transform.scale(img, size, srf)
    block["melee"]["resource"] = srf
    
    img = load("peaUI")
    img = img.convert_alpha(img)
    srf = Surface(size, SRCALPHA)
    transform.scale(img, size, srf)
    block["ranged"]["resource"] = srf


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

    load_pea(IMAGE_RESOURCE["entities"], 0)
    load_pea(IMAGE_RESOURCE["entities"], 1)
    load_pea(IMAGE_RESOURCE["entities"], 2)
    load_pea(IMAGE_RESOURCE["entities"], 3)

    load_ui(IMAGE_RESOURCE["ui"])
