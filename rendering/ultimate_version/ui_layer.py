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

        self.current_health = 1.0
        self.current_seed_count_melee = 1.0
        self.current_seed_count_ranged = 1.0


    # call once for each player
    def render(self, render_target: Surface, world: World):
        for i in range(4):
            p = world.players[i]
            self.draw_ui_for_player(i, render_target, p)

    def draw_ui_for_player(self, i: int, target: Surface, player: Player):
        # Health
        health_percent = player.hp / PLAYER_LIFE

        # Seeds
        self.current_seed_count_melee = player.get_seeds(SeedType.melee) / self.max_seeds
        self.current_seed_count_ranged = player.get_seeds(SeedType.ranged) / self.max_seeds
        target.fill(COLOR_PLAYERS[i], (self.fill_origins[i], (target.get_width(), target.get_height() * self.current_health)))
        target.fill(COLOR_BACKGROUND_SECONDARY, (self.fill_origins[i], self.hp_area))

    def hp_fill(self, target: Surface, i: int, percent: float):
        flip = i < 2
        ox, oy = self.fill_origins[i]
        w, h = self.hp_area
        if flip:
            upper_color = COLOR_BACKGROUND_SECONDARY
            lower_color = COLOR_PLAYERS[i]
            percent = 1 - percent
        else:
            upper_color = COLOR_PLAYERS[i]
            lower_color = COLOR_BACKGROUND_SECONDARY

        target.fill(color=upper_color,
                    rect=((ox, oy),
                          (w, h * percent)))
        target.fill(color=lower_color,
                    rect=((ox, oy),
                          (w, h * (1-percent))))
