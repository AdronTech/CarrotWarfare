from rendering.ultimate_version.renderer import *


class EntityLayer:
    def __init__(self, renderer: UltimateRenderer, arena_subsurface: Surface):
        self.parent_renderer = renderer
        self.arena_subsurface = arena_subsurface

    def render(self, world: World):
        # for every horizontal line
        for y in range(WORLD_DIMENSION["height"]):

            # get all items in tile
            def extract_from_tile(tile: Tile, tx, ty):
                for e in tile.entities:
                    yield e
                if "environment" in tile.render_flags:
                    yield tile.render_flags["environment"], tx, ty

            # generate rows
            row = [e for x in range(WORLD_DIMENSION["width"])
                   for e in extract_from_tile(world.grid[x][y], x, y)]  # type: list[Entity]

            # depth sort
            def depth_sort(e):
                if issubclass(type(e), Entity):
                    return e.pos.y
                else:
                    return e[2] + 0.5

            row = sorted(row, key=depth_sort)

            shadow_block = IMAGE_RESOURCE["juice"]["shadow"]
            # draw
            for entity in row:
                e_type = type(entity)
                if e_type is Player:
                    self.arena_subsurface.blit(shadow_block[str(entity.alliance)],
                                               (entity.pos.x * TILE_SIZE + shadow_block["offset"][0],
                                                entity.pos.y * TILE_SIZE + shadow_block["offset"][1]))
                    self.render_player(entity)
                elif e_type is Carrot:
                    self.arena_subsurface.blit(shadow_block[str(entity.alliance)],
                                               (entity.pos.x * TILE_SIZE + shadow_block["offset"][0],
                                                entity.pos.y * TILE_SIZE + shadow_block["offset"][1]))
                    self.render_carrot(entity)
                elif e_type is Sprout:
                    self.arena_subsurface.blit(shadow_block[str(entity.alliance)],
                                               (entity.pos.x * TILE_SIZE + shadow_block["offset"][0],
                                                entity.pos.y * TILE_SIZE + shadow_block["offset"][1]))
                    self.render_sprout(entity)
                elif e_type is Bullet:
                    self.arena_subsurface.blit(shadow_block[str(entity.alliance)],
                                               (entity.pos.x * TILE_SIZE + shadow_block["offset"][0],
                                                entity.pos.y * TILE_SIZE + shadow_block["offset"][1]))
                    self.render_pea(entity)
                else:
                    surf, x, y = entity
                    self.arena_subsurface.blit(surf, (int(x * TILE_SIZE - surf.get_width() / 2),
                                                      int((y + 0.5) * TILE_SIZE - surf.get_height())))

    def render_player(self, player: Player):
        events = []
        for e in player.events:
            if e["name"] == "death":
                events.append("death")
            elif e["name"] == "attack":
                events.append("attack")
            elif e["name"] == "move":
                events.append("move")
            elif e["name"] == "call":
                events.append("call")
        player.events.clear()

        if "death" in events:
            if "animator" in player.render_flags:
                player.render_flags["animator"].set_animation("state_die", True)
            else:
                player.render_flags["animator"] = EntityAnimator(player, "state_die")
        if "attack" in events:
            player.hard_lock = IMAGE_RESOURCE["entities"]["player_generic"]["attack_hard_lock"]
            player.soft_lock = IMAGE_RESOURCE["entities"]["player_generic"]["attack_soft_lock"]
            if "animator" in player.render_flags:
                player.render_flags["animator"].set_animation("state_attack")
            else:
                player.render_flags["animator"] = EntityAnimator(player, "state_attack")
        if "move" in events:
            if "animator" in player.render_flags:
                player.render_flags["animator"].set_animation("state_walk", 500)
            else:
                player.render_flags["animator"] = EntityAnimator(player, "state_walk", 500)
        if "call" in events:
            player.hard_lock = IMAGE_RESOURCE["entities"]["player_generic"]["call_hard_lock"]
            player.soft_lock = IMAGE_RESOURCE["entities"]["player_generic"]["call_soft_lock"]
            if "animator" in player.render_flags:
                player.render_flags["animator"].set_animation("state_attack", 500, True)
            else:
                player.render_flags["animator"] = EntityAnimator(player, "state_attack", 500)

        image = None
        resources = IMAGE_RESOURCE["entities"]
        if "animator" in player.render_flags:
            if player.dir.x < 0:
                image = player.render_flags["animator"].get_frame(True)
            else:
                image = player.render_flags["animator"].get_frame(False)
            if not image:
                del player.render_flags["animator"]
        if not image:
            if player.dir.x < 0:
                image = resources["player" + str(player.alliance)]["state_stand"]["left"]["frame0"]
            else:
                image = resources["player" + str(player.alliance)]["state_stand"]["right"]["frame0"]

        angle = -player.dir.as_polar()[1]
        draw.arc(self.arena_subsurface,
                 COLOR_PLAYERS[player.alliance],
                 Rect(int((player.pos.x - player.attack_range) * TILE_SIZE),
                      int((player.pos.y - player.attack_range) * TILE_SIZE),
                      int(player.attack_range * TILE_SIZE * 2),
                      int(player.attack_range * TILE_SIZE * 2)),
                 (angle - player.attack_angle / 2) * pi / 180,
                 (angle + player.attack_angle / 2) * pi / 180,
                 5)

        self.arena_subsurface.blit(image,
                                   (int(player.pos.x *
                                        TILE_SIZE + resources["player_generic"]["offset"][0]),
                                    int(player.pos.y *
                                        TILE_SIZE + resources["player_generic"]["offset"][1])))

    def render_carrot(self, carrot: Carrot):
        events = []
        for e in carrot.events:
            if e["name"] == "death":
                events.append("death")
            elif e["name"] == "attack":
                events.append("attack")
            elif e["name"] == "move":
                events.append("move")
        carrot.events.clear()

        if "death" in events:
            if "animator" in carrot.render_flags:
                carrot.render_flags["animator"].set_animation("state_die", True)
            else:
                carrot.render_flags["animator"] = EntityAnimator(carrot, "state_die")
        if "attack" in events:
            carrot.hard_lock = IMAGE_RESOURCE["entities"]["sprout_generic"]["attack_hard_lock"]
            carrot.soft_lock = IMAGE_RESOURCE["entities"]["sprout_generic"]["attack_soft_lock"]
            if "animator" in carrot.render_flags:
                carrot.render_flags["animator"].set_animation("state_attack", True)
            else:
                carrot.render_flags["animator"] = EntityAnimator(carrot, "state_attack")
        if "move" in events:
            if "animator" in carrot.render_flags:
                carrot.render_flags["animator"].set_animation("state_walk", 500)
            else:
                carrot.render_flags["animator"] = EntityAnimator(carrot, "state_walk", 500)

        image = None
        resources = IMAGE_RESOURCE["entities"]
        if "animator" in carrot.render_flags:
            if carrot.dir.x < 0:
                image = carrot.render_flags["animator"].get_frame(True)
            else:
                image = carrot.render_flags["animator"].get_frame(False)
            if not image:
                del carrot.render_flags["animator"]
        if not image:
            if carrot.dir.x < 0:
                image = resources["carrot" + str(carrot.alliance)]["state_stand"]["left"]["frame0"]
            else:
                image = resources["carrot" + str(carrot.alliance)]["state_stand"]["right"]["frame0"]

        self.arena_subsurface.blit(image,
                                   (int(carrot.pos.x *
                                        TILE_SIZE + resources["carrot_generic"]["offset"][0]),
                                    int(carrot.pos.y *
                                        TILE_SIZE + resources["carrot_generic"]["offset"][1])))

    def render_sprout(self, sprout: Sprout):
        events = []
        for e in sprout.events:
            if e["name"] == "death":
                events.append("death")
            elif e["name"] == "attack":
                events.append("attack")
            elif e["name"] == "move":
                events.append("move")
        sprout.events.clear()

        if "death" in events:
            if "animator" in sprout.render_flags:
                sprout.render_flags["animator"].set_animation("state_die", True)
            else:
                sprout.render_flags["animator"] = EntityAnimator(sprout, "state_die")
        if "attack" in events:
            sprout.hard_lock = IMAGE_RESOURCE["entities"]["sprout_generic"]["attack_hard_lock"]
            sprout.soft_lock = IMAGE_RESOURCE["entities"]["sprout_generic"]["attack_soft_lock"]
            if "animator" in sprout.render_flags:
                sprout.render_flags["animator"].set_animation("state_attack", True)
            else:
                sprout.render_flags["animator"] = EntityAnimator(sprout, "state_attack")
        if "move" in events:
            if "animator" in sprout.render_flags:
                sprout.render_flags["animator"].set_animation("state_walk", 500)
            else:
                sprout.render_flags["animator"] = EntityAnimator(sprout, "state_walk", 500)

        image = None
        resources = IMAGE_RESOURCE["entities"]
        if "animator" in sprout.render_flags:
            if sprout.dir.x < 0:
                image = sprout.render_flags["animator"].get_frame(True)
            else:
                image = sprout.render_flags["animator"].get_frame(False)
            if not image:
                del sprout.render_flags["animator"]
        if not image:
            if sprout.dir.x < 0:
                image = resources["sprout" + str(sprout.alliance)]["state_stand"]["left"]["frame0"]
            else:
                image = resources["sprout" + str(sprout.alliance)]["state_stand"]["right"]["frame0"]

        self.arena_subsurface.blit(image,
                                   (int(sprout.pos.x *
                                        TILE_SIZE + resources["sprout_generic"]["offset"][0]),
                                    int(sprout.pos.y *
                                        TILE_SIZE + resources["sprout_generic"]["offset"][1])))

    def render_pea(self, pea: Bullet):

        image = IMAGE_RESOURCE["entities"]["pea" + str(pea.alliance)]["resource"]

        self.arena_subsurface.blit(image,
                                   (int(pea.pos.x *
                                        TILE_SIZE + IMAGE_RESOURCE["entities"]["pea_generic"]["offset"][0]),
                                    int(pea.pos.y *
                                        TILE_SIZE + IMAGE_RESOURCE["entities"]["pea_generic"]["offset"][1])))
