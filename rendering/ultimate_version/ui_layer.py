from rendering.ultimate_version.renderer import *


class UILayer:
    def __init__(self, renderer: UltimateRenderer, main_surface: Surface):

        ui_x_left = 0
        ui_x_right = ARENA_SURFACE_SIZE[0] + HUD_AREA[0]
        ui_y_top = 0
        ui_y_bottom = HUD_AREA[1]

        self.hp_area = (RENDER_RESOLUTION[0]/2, RENDER_RESOLUTION[1]/2)
        self.fill_origins = (
            (0, 0), (self.hp_area[0], 0), (0, self.hp_area[1]), (self.hp_area[0], self.hp_area[1])
        )
        self.hp_show = [0] * 4
        self.main_surface = main_surface
        self.parent_renderer = renderer
        self.current_health = 1.0
        self.current_seed_count_melee = 1.0
        self.current_seed_count_ranged = 1.0

        for i in range(4):
            self.hp_fill(i, self.hp_show[i])

    def render(self, world: World):
        for i in range(4):
            player = world.players[i]  # type: Player
            if player:
                diff = (player.hp - self.hp_show[i])
                if abs(diff) > 1:
                    self.hp_show[i] += diff*0.1
                else:
                    self.hp_show[i] = player.hp
                self.hp_fill(i, self.hp_show[i])
                # self.draw_hud(i, world.players[i])
            else:
                self.hp_fill(i, 0)

    def draw_hud(self, i: int, player: Player):
        # Seeds
        self.current_seed_count_melee = player.get_seeds(SeedType.melee) / self.max_seeds
        self.current_seed_count_ranged = player.get_seeds(SeedType.ranged) / self.max_seeds

    def hp_fill(self, i: int, hp: int):
        lower_hud = i < 2
        x, oy = self.fill_origins[i]
        w, h = self.hp_area
        if lower_hud:
            c_lower = COLOR_PLAYERS[i]
            c_upper = COLOR_BACKGROUND_SECONDARY
            percent = hp/PLAYER_LIFE
        else:
            c_lower = COLOR_BACKGROUND_SECONDARY
            c_upper = COLOR_PLAYERS[i]
            percent = 1 - hp/PLAYER_LIFE
        y_lower = oy
        h_lower = int(h*percent)
        r_lower = (x, y_lower), (w, h_lower)
        y_upper = y_lower+h_lower
        h_upper = h-h_lower
        r_upper = (x, y_upper), (w, h_upper)
        print(h, h_lower, h_upper)

        self.main_surface.fill(color=c_lower,
                    rect=r_lower)
        self.main_surface.fill(color=c_upper,
                    rect=r_upper)
