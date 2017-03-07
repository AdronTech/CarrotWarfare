from pygame import Surface, error, image
from os.path import join
from rendering.constants import IMAGE_RESOURCE


def load(path: str) -> Surface:
    try:
        img = image.load_basic(join('assets/sprites', path))
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
                block_cache[key]["offset"] = (Surface(block_cache[key]["resource"]).get_width() / -2,
                                              Surface(block_cache[key]["resource"]).get_height() * -1)
