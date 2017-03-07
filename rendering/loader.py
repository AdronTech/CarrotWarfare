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


def load_all():
    for block in IMAGE_RESOURCE.keys():
        block_cache = IMAGE_RESOURCE[block]
        for key in block_cache.keys():
            block_cache[key]["resource"] = load("playerTest")  # load(key)
            if block == "entities":
                ratio = block_cache[key]["resource"].get_width() / float(block_cache[key]["resource"].get_height())
                block_cache[key]["scale"] = (int(TILE_SIZE * ratio), int(TILE_SIZE))

                block_cache[key]["offset"] = (block_cache[key]["scale"][0] / -2,
                                              block_cache[key]["scale"][1] * -1)
                block_cache[key]["resource"] = transform.scale(block_cache[key]["resource"],
                                                               block_cache[key]["scale"])
