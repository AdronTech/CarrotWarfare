from game.world import WORLD_DIMENSION

# Blue, Red, Green, Amber @ Material Palette
COLOR_PLAYERS = [(33, 150, 243), (244, 67, 54), (76, 175, 80), (255, 193, 7)]
COLOR_BACKGROUND = (250, 250, 250)
COLOR_BACKGROUND_SECONDARY = (224, 224, 224)

DISPLAY_RESOLUTION = (1280, 720)

SCREEN_SHAKE_OFFSET = (min(DISPLAY_RESOLUTION[0], DISPLAY_RESOLUTION[1]) / 20,
                       min(DISPLAY_RESOLUTION[0], DISPLAY_RESOLUTION[1]) / 20)
SCREEN_SHAKE_COUNT = 3

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

IMAGE_RESOURCE = {
    "entities": {
        "player0": {},
        "player1": {},
        "player2": {},
        "player3": {},

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
