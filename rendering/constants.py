# Blue, Red, Green, Amber @ Material Palette
COLOR_PLAYERS = [(33, 150, 243), (244, 67, 54), (76, 175, 80), (255, 193, 7)]
COLOR_PLAYERS_SECONDARY = [(25, 118, 210), (211, 47, 47), (56, 142, 60), (255, 160, 0)]
COLOR_BACKGROUND = (250, 250, 250)
COLOR_BACKGROUND_SECONDARY = (224, 224, 224)

DISPLAY_RESOLUTION = (1280, 720)

WORLD_DIMENSION = {"width": 27, "height": 17}

SCREEN_SHAKE_OFFSET = (min(DISPLAY_RESOLUTION[0], DISPLAY_RESOLUTION[1]) / 20,
                       min(DISPLAY_RESOLUTION[0], DISPLAY_RESOLUTION[1]) / 20)
TILE_SIZE = min(DISPLAY_RESOLUTION[0] / float(WORLD_DIMENSION["width"]),
                DISPLAY_RESOLUTION[1] / float(WORLD_DIMENSION["height"]))
MAIN_SURFACE_SIZE = (DISPLAY_RESOLUTION[0] + SCREEN_SHAKE_OFFSET[0] * 2,
                     DISPLAY_RESOLUTION[1] + SCREEN_SHAKE_OFFSET[1] * 2)
SUB_SURFACE_SIZE = (TILE_SIZE * WORLD_DIMENSION["width"],
                    TILE_SIZE * WORLD_DIMENSION["height"])
SUB_SURFACE_BORDER = ((DISPLAY_RESOLUTION[0] - SUB_SURFACE_SIZE[0]) / 2,
                      (DISPLAY_RESOLUTION[1] - SUB_SURFACE_SIZE[1]) / 2)
SUB_SURFACE_POSITION = (SUB_SURFACE_BORDER[0] + SCREEN_SHAKE_OFFSET[0],
                        SUB_SURFACE_BORDER[1] + SCREEN_SHAKE_OFFSET[1])
UI_SUBSURFACE_SIZE = (SUB_SURFACE_BORDER[0], SUB_SURFACE_SIZE[1] / 2)
UI_SEED_SURFACE_SIZE = (UI_SUBSURFACE_SIZE[0] / 4, UI_SUBSURFACE_SIZE[1] / 2)


def get_ultimate_surface():
    from pygame import Surface
    srf = Surface(MAIN_SURFACE_SIZE)
    srf.fill(COLOR_PLAYERS[0], ((0, 0),
                                (MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2)))
    srf.fill(COLOR_PLAYERS[1], ((MAIN_SURFACE_SIZE[0] / 2, 0),
                                (MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2)))
    srf.fill(COLOR_PLAYERS[2], ((0, MAIN_SURFACE_SIZE[1] / 2),
                                (MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2)))
    srf.fill(COLOR_PLAYERS[3], ((MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2),
                                (MAIN_SURFACE_SIZE[0] / 2, MAIN_SURFACE_SIZE[1] / 2)))
    return srf


IMAGE_RESOURCE = {
    "entities": {
        "player0": {
            "name": "player0"
        },
        "player1": {
            "name": "player1"
        },
        "player2": {
            "name": "player2"
        },
        "player3": {
            "name": "player3"
        },

        "carrot0": {},
        "carrot1": {},
        "carrot2": {},
        "carrot3": {}
    },
    "tiles": {

    },
    "juice": {

    }
}
