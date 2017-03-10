from rendering.ultimate_version.renderer import *

ICON_BORDER_COLOR = (0, 0, 0)
AMMO_BAR_COLOR = (0, 0, 0)


class UILayer:
    def __init__(self, renderer: UltimateRenderer, main_surface: Surface):
        self.parent_renderer = renderer
        self.main_surface = main_surface
        self.hp_area = (RENDER_RESOLUTION[0]/2, RENDER_RESOLUTION[1]/2)
        self.hp_show = [0] * 4
        self.hp_fill_origins = (
            (0, 0),
            (self.hp_area[0], 0),
            (0, self.hp_area[1]),
            (self.hp_area[0], self.hp_area[1])
        )

        self.hud_center = int(ARENA_SURFACE_PADDING[0] / 2)
        self.icon_w = int(ARENA_SURFACE_PADDING[0] / 3)
        self.border_w = int(0.16 * self.icon_w)
        self.bar_w = int(0.2 * self.icon_w)
        self.icon_hpad = int(self.border_w * 1)
        self.icon_vpad = int(self.icon_w * 0.6)
        self.hud_origins = (
            (0, 0),
            (HUD_AREA[0]+ARENA_SURFACE_SIZE[0], 0),
            (0, HUD_AREA[1]),
            (HUD_AREA[0]+ARENA_SURFACE_SIZE[0], HUD_AREA[1])
        )

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

    def hp_fill(self, id: int, hp: int):
        lower_hud = id < 2
        x, oy = self.hp_fill_origins[id]
        w, h = self.hp_area
        if lower_hud:
            c_lower = COLOR_PLAYERS[id]
            c_upper = COLOR_BACKGROUND_SECONDARY
            percent = hp/PLAYER_LIFE
        else:
            c_lower = COLOR_BACKGROUND_SECONDARY
            c_upper = COLOR_PLAYERS[id]
            percent = 1 - hp/PLAYER_LIFE
        y_lower = oy
        h_lower = int(h*percent)
        r_lower = (x, y_lower), (w, h_lower)
        y_upper = y_lower+h_lower
        h_upper = h-h_lower
        r_upper = (x, y_upper), (w, h_upper)
        self.main_surface.fill(color=c_lower, rect=r_lower)
        self.main_surface.fill(color=c_upper, rect=r_upper)

    def draw_hud(self, id: int, seed_mode: int, seeds):
        icon_l = self.hud_center - self.icon_w - self.icon_hpad
        icon_r = self.hud_center + self.icon_hpad
        if id < 2:
            icon_y = self.icon_vpad
            bar_y = (icon_y+self.icon_w, HUD_AREA[1]-self.icon_w)
        else:
            icon_r = self.hud_center + self.icon_hpad
            icon_y = HUD_AREA[1]-self.icon_vpad-self.icon_w
            bar_y = (icon_y, self.icon_vpad)
        # r_l
        self.draw_ammo_bar(origin=self.hud_origins[id],
                           bar_x=icon_l + self.icon_w / 2,
                           bar_y=bar_y,
                           width=self.bar_w,
                           fill=seeds[0])
        self.draw_ammo_icon(id=id,
                            origin=self.hud_origins[id],
                            offset=(icon_l, icon_y),
                            selected=seed_mode is 0)
        # r_r
        self.draw_ammo_bar(origin=self.hud_origins[id],
                           bar_x=icon_r + self.icon_w / 2,
                           bar_y=bar_y,
                           width=self.bar_w,
                           fill=seeds[1])
        self.draw_ammo_icon(id=id,
                            origin=self.hud_origins[id],
                            offset=(icon_r, icon_y),
                            selected=seed_mode is 1)

    def draw_ammo_icon(self, id: int, origin, offset, selected):
        hx, hy = origin
        x, y = offset
        rect = (hx + x, hy + y), (self.icon_w, self.icon_w)
        self.main_surface.fill(COLOR_PLAYERS_DARK[id], rect)
        if selected:
            draw.rect(self.main_surface, ICON_BORDER_COLOR, rect, self.border_w)

    def draw_ammo_bar(self, origin, bar_x, bar_y, width, fill):
        hx, hy = origin
        start, end_max = bar_y
        end = start + (end_max-start) * (fill/PLAYER_SEED_POUCH)
        draw.line(self.main_surface,
                  AMMO_BAR_COLOR,
                  (hx + bar_x, hy + start),
                  (hx + bar_x, hy + end),
                  width)
        draw.line(self.main_surface,
                  AMMO_BAR_COLOR,
                  (hx + bar_x - width, hy + end),
                  (hx + bar_x + width, hy + end),
                  width*2)
