from rendering.ultimate_version.renderer import *


class UILayer:
    def __init__(self, renderer: UltimateRenderer, main_surface: Surface):
        self.hp_area = (RENDER_RESOLUTION[0]/2, RENDER_RESOLUTION[1]/2)
        self.fill_origins = (
            (0, 0),
            (self.hp_area[0], 0),
            (0, self.hp_area[1]),
            (self.hp_area[0], self.hp_area[1])
        )
        self.hud_origins = (
            (0, 0),
            (HUD_AREA[0]+ARENA_SURFACE_SIZE[0], 0),
            (0, HUD_AREA[1]),
            (HUD_AREA[0]+ARENA_SURFACE_SIZE[0], HUD_AREA[1])
        )
        self.hp_show = [0] * 4
        self.main_surface = main_surface
        self.parent_renderer = renderer

    def render(self, world: World):
        for i in range(4):
            player = world.players[i]  # type: Player
            if player:
                # draw hp
                diff = (player.hp - self.hp_show[i])
                if abs(diff) > 1:
                    self.hp_show[i] += diff*0.1
                else:
                    self.hp_show[i] = player.hp
                self.hp_fill(i, self.hp_show[i])
                self.draw_hud(i, player.seed_mode.value, player.seeds)
            else:
                self.hp_fill(i, 0)

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
        self.main_surface.fill(color=c_lower, rect=r_lower)
        self.main_surface.fill(color=c_upper, rect=r_upper)

    def draw_hud(self, i: int, seed_mode: int, seeds):
        hud_half_point = int(ARENA_SURFACE_PADDING[0] / 2)
        icon_w = int(ARENA_SURFACE_PADDING[0] / 4)
        border_w = int(0.175 * icon_w)
        bar_w = int(0.2 * icon_w)
        icon_hpad = int(border_w * 1)
        icon_vpad = int(icon_w * 1.2)
        hx, hy = self.hud_origins[i]
        if i < 2:
            icon_l = hud_half_point-icon_w-icon_hpad
            icon_r = hud_half_point+icon_hpad
            icon_y = icon_vpad
            bar_y = (icon_y+icon_w, HUD_AREA[1]-icon_w)
        else:
            icon_l = hud_half_point-icon_w-icon_hpad
            icon_r = hud_half_point+icon_hpad
            icon_y = HUD_AREA[1]-(icon_vpad-icon_w)
            bar_y = (icon_y, hy + icon_vpad)
        # r_l
        r_l = (hx+icon_l, hy+icon_y), (icon_w, icon_w)
        self.main_surface.fill((255, 255, 255), r_l)
        if seed_mode is 0:
            draw.rect(self.main_surface, (0, 0, 0), r_l, border_w)
        self.draw_ammo(hx+icon_l+icon_w/2, hy+bar_y[0], hy+bar_y[1], seeds[0], bar_w)
        # r_r
        r_r = (hx+icon_r, hy+icon_y), (icon_w, icon_w)
        self.main_surface.fill((255, 255, 255), r_r)
        if seed_mode is 1:
            draw.rect(self.main_surface, (0, 0, 0), r_r, border_w)
        self.draw_ammo(hx+icon_r+icon_w/2, hy+bar_y[0], hy+bar_y[1], seeds[1], bar_w)

    def draw_ammo(self, x, start_y, end_y, fill, width=5):
        end_y = start_y + (end_y-start_y) * fill/PLAYER_SEED_POUCH
        draw.line(self.main_surface, (0, 0, 0), (x, start_y), (x, end_y), width)
        draw.line(self.main_surface, (0, 0, 0), (x-width, end_y), (x+width, end_y), width*2)
