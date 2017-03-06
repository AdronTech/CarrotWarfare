from pygame import Surface, image, error


def load_from_image(path: str) -> Surface:
    try:
        img = image.load(path)
    except error:
        raise SystemExit("Could not load image from {}".format(path))
    img.convert_alpha(img)
    return img
