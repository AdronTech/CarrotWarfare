from rendering.ultimate_version.renderer import *


class UILayer:
    def __init__(self, renderer: UltimateRenderer, player_ui_surfaces: [Surface]):

        ui_x_left = 0
        ui_x_right = ARENA_SURFACE_SIZE[0] + HUD_AREA[0]
        ui_y_top = 0
        ui_y_bottom = HUD_AREA[1]

        self.hp_area = (RENDER_RESOLUTION[0]/2, RENDER_RESOLUTION[1]/2)
        self.fill_origins = (
            (0, 0), (self.hp_area[0], 0), (0, self.hp_area[1]), (self.hp_area[0], self.hp_area[1])
        )

        self.parent_renderer = renderer
        self.player_ui_surfaces = player_ui_surfaces

        self.max_health = 100.0
        self.max_seeds = 200.0

        self.current_health = 1.0
        self.current_seed_count_melee = 1.0
        self.current_seed_count_ranged = 1.0


    # call once for each player
    def draw_ui_for_player(self, i: int, target: Surface, player: Player):
        # Health
        self.current_health = player.hp / self.max_health
        # Seeds
        self.current_seed_count_melee = player.get_seeds(SeedType.melee) / self.max_seeds
        self.current_seed_count_ranged = player.get_seeds(SeedType.ranged) / self.max_seeds
        target.fill(COLOR_PLAYERS[i], ((0, 0), (target.get_width(), target.get_height() * self.current_health)))

    def render(self, render_target: Surface, world: World):
        for i in range(2):
            player = world.entities[i]
            self.draw_ui_for_player(i, self.player_ui_surfaces[i], player)
            render_target.fill(COLOR_PLAYERS[i], (self.fill_origins[i], self.hp_area))
            render