# Blue, Red, Green, Amber @ Material Palette
COLOR_PLAYERS = [(33, 150, 243), (244, 67, 54), (76, 175, 80), (255, 193, 7)]
COLOR_PLAYERS_DARK = [(25, 118, 210), (211, 47, 47), (56, 142, 60), (255, 160, 0)]
COLOR_PLAYERS_LIGHT = [(100, 181, 246), (229, 115, 115), (129, 199, 132), (255, 213, 79)]
REPLACEMENT_COLOR_DARK = (1, 1, 1)
REPLACEMENT_COLOR_LIGHT = (2, 2, 2)
COLOR_BACKGROUND = (250, 250, 250)
COLOR_BACKGROUND_SECONDARY = (224, 224, 224)

RENDER_RESOLUTION = (1600, 900)

WORLD_DIMENSION = {"width": 27, "height": 17}

SCREEN_SHAKE_OFFSET = (min(RENDER_RESOLUTION[0], RENDER_RESOLUTION[1]) / 20,
                       min(RENDER_RESOLUTION[0], RENDER_RESOLUTION[1]) / 20)

TILE_SIZE = int(min(RENDER_RESOLUTION[0] / float(WORLD_DIMENSION["width"]),
                    RENDER_RESOLUTION[1] / float(WORLD_DIMENSION["height"])))
ARENA_SURFACE_SIZE = (TILE_SIZE * WORLD_DIMENSION["width"],
                      TILE_SIZE * WORLD_DIMENSION["height"])
ARENA_SURFACE_PADDING = ((RENDER_RESOLUTION[0] - ARENA_SURFACE_SIZE[0]) / 2,
                         (RENDER_RESOLUTION[1] - ARENA_SURFACE_SIZE[1]) / 2)
HUD_AREA = (ARENA_SURFACE_PADDING[0], ARENA_SURFACE_SIZE[1] / 2)

# Growing == Idle for player
IMAGE_RESOURCE = {
    "entities": {
        "player_generic": {"name": "player",
                           "offset": None,
                           "call_hard_lock": 0,
                           "call_soft_lock": 0.5,

                           "attack_hard_lock": 0.25,
                           "attack_soft_lock": 0.5},

        "carrot_generic": {"name": "carrot",
                           "offset": None,
                           "attack_hard_lock": 0.2,
                           "attack_soft_lock": 0.3},

        "sprout_generic": {"name": "sprout",
                           "offset": None,
                           "attack_hard_lock": 0.25,
                           "attack_soft_lock": 1},
        "player0": {
            "alliance": 0,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},
        "player1": {
            "alliance": 1,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},
        "player2": {
            "alliance": 2,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},
        "player3": {
            "alliance": 3,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},

        "carrot0": {
            "alliance": 0,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},
        "carrot1": {
            "alliance": 1,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},
        "carrot2": {
            "alliance": 2,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},
        "carrot3": {
            "alliance": 3,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},

        "sprout0": {
            "alliance": 0,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},
        "sprout1": {
            "alliance": 1,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},
        "sprout2": {
            "alliance": 2,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},
        "sprout3": {
            "alliance": 3,
            "state_stand": {
                "left": {"name": "stand",
                         "frame0": None},
                "right": {"name": "stand",
                          "frame0": None}},
            "state_die": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_walk": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_attack": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}},
            "state_growing": {
                "left": {"name": "die",
                         "frame0": None,
                         "frame1": None,
                         "frame2": None,
                         "frame3": None},
                "right": {"name": "die",
                          "frame0": None,
                          "frame1": None,
                          "frame2": None,
                          "frame3": None}}},

        "pea_generic": {"name": "pea",
                        "offset": None},
        "pea0": {},
        "pea1": {},
        "pea2": {},
        "pea3": {}
    },
    "tiles": {

    },
    "ui": {
        "melee": {"resource": None},
        "ranged": {"resource": None}
    }
}
