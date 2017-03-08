from rendering.ultimate_version.renderer import *


class UILayer:
    def __init__(self, renderer: UltimateRenderer, player_ui_surfaces: [Surface]):
        self.parent_renderer = renderer
        self.player_ui_surfaces = player_ui_surfaces

        self.max_health = 40.0
        self.max_seeds = 200.0

        self.current_health = 1.0
        self.current_seed_count_melee = 1.0
        self.current_seed_count_ranged = 1.0

    # call once for each player
    def draw_ui_for_player(self, i: int, target: Surface, player: Player):
        target.fill(COLOR_BACKGROUND_SECONDARY)

        # Health
        self.current_health = player.hp / self.max_health
        # Seeds
        self.current_seed_count_melee = player.get_seeds(SeedType.melee) / self.max_seeds
        self.current_seed_count_ranged = player.get_seeds(SeedType.ranged) / self.max_seeds

        # ask Saman for advice
        # minimize
        def draw(bottom: bool):
            if not bottom:
                target.fill(COLOR_PLAYERS[i], ((0, 0), (target.get_width(), target.get_height() * self.current_health)))
                if player.seed_mode == SeedType.melee:
                    target.fill(COLOR_BACKGROUND, ((UI_SEED_SURFACE_SIZE[0],
                                                    UI_SEED_SURFACE_SIZE[0]),
                                                   (UI_SEED_SURFACE_SIZE[0],
                                                    UI_SEED_SURFACE_SIZE[1] * self.current_seed_count_melee)))
                    target.fill(COLOR_PLAYERS_SECONDARY[i], ((UI_SEED_SURFACE_SIZE[0] * 2,
                                                              UI_SEED_SURFACE_SIZE[0]),
                                                             (UI_SEED_SURFACE_SIZE[0],
                                                              UI_SEED_SURFACE_SIZE[
                                                                  1] * self.current_seed_count_ranged)))
                elif player.seed_mode == SeedType.ranged:
                    target.fill(COLOR_PLAYERS_SECONDARY[i], ((UI_SEED_SURFACE_SIZE[0],
                                                              UI_SEED_SURFACE_SIZE[0]),
                                                             (UI_SEED_SURFACE_SIZE[0],
                                                              UI_SEED_SURFACE_SIZE[1] * self.current_seed_count_melee)))
                    target.fill(COLOR_BACKGROUND, ((UI_SEED_SURFACE_SIZE[0] * 2,
                                                    UI_SEED_SURFACE_SIZE[0]),
                                                   (UI_SEED_SURFACE_SIZE[0],
                                                    UI_SEED_SURFACE_SIZE[1] * self.current_seed_count_ranged)))
            else:
                if player.seed_mode == SeedType.melee:
                    target.fill(COLOR_BACKGROUND, ((UI_SEED_SURFACE_SIZE[0],
                                                    UI_SEED_SURFACE_SIZE[0]),
                                                   (UI_SEED_SURFACE_SIZE[0],
                                                    UI_SEED_SURFACE_SIZE[1] * self.current_seed_count_melee)))
                    target.fill(COLOR_PLAYERS_SECONDARY[i], ((UI_SEED_SURFACE_SIZE[0] * 2,
                                                              UI_SEED_SURFACE_SIZE[0]),
                                                             (UI_SEED_SURFACE_SIZE[0],
                                                              UI_SEED_SURFACE_SIZE[
                                                                  1] * self.current_seed_count_ranged)))
                elif player.seed_mode == SeedType.ranged:
                    target.fill(COLOR_PLAYERS_SECONDARY[i], ((UI_SEED_SURFACE_SIZE[0],
                                                              UI_SEED_SURFACE_SIZE[0]),
                                                             (UI_SEED_SURFACE_SIZE[0],
                                                              UI_SEED_SURFACE_SIZE[1] * self.current_seed_count_melee)))
                    target.fill(COLOR_BACKGROUND, ((UI_SEED_SURFACE_SIZE[0] * 2,
                                                    UI_SEED_SURFACE_SIZE[0]),
                                                   (UI_SEED_SURFACE_SIZE[0],
                                                    UI_SEED_SURFACE_SIZE[1] * self.current_seed_count_ranged)))

        draw(False)  # i == 0 or i == 1

    def render(self, world: World):
        for i in range(world.player_count):
            player = world.entities[i]
            self.draw_ui_for_player(i, self.player_ui_surfaces[i], player)
