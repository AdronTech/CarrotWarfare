from pygame import Surface, error, image
from os.path import join
from rendering.constants import IMAGE_RESOURCE, TILE_SIZE
from pygame import transform


def load(path: str) -> Surface:
    try:
        img = image.load_extended(join('assets/sprites', path + ".png"))
    except error:
        raise SystemExit("Could not load image from {}".format(path))

    img.convert_alpha(img)
    return img


def put_values_for_entity(block: dict):
    block["resource"] = load(block["name"])
    ratio = block["resource"].get_width() / float(block["resource"].get_height())
    block["scale"] = (int(TILE_SIZE * ratio), int(TILE_SIZE))
    block["offset"] = (block["scale"][0] / -2,
                       block["scale"][1] * -1)
    block["resource"] = transform.scale(block["resource"],
                                        block["scale"])


def load_all():
    put_values_for_entity(IMAGE_RESOURCE["entities"]["player0"])
    put_values_for_entity(IMAGE_RESOURCE["entities"]["player1"])
    put_values_for_entity(IMAGE_RESOURCE["entities"]["player2"])
    put_values_for_entity(IMAGE_RESOURCE["entities"]["player3"])
