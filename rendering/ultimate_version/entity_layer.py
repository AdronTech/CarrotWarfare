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
                    for env_object in tile.render_flags["environment"]:
                        yield env_object, tx, ty

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

            # draw
            for entity in row:
                e_type = type(entity)
                if e_type is Player:
                    self.render_player(entity)
                elif e_type is Carrot:
                    self.render_carrot(entity)
                elif e_type is Sprout:
                    self.render_sprout(entity)
                elif e_type is Bullet:
                    pass
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
            elif e["name"] == "plant_request":
                if "allowed" in e:
                    events.append("plant_request")

        if "death" in events:
            if "animator" in player.render_flags:
                player.render_flags["animator"].set_animation("state_die")
            else:
                player.render_flags["animator"] = EntityAnimator(player, "state_die")
        if "attack" in events:
            if "animator" in player.render_flags:
                player.render_flags["animator"].set_animation("state_attack")
            else:
                player.render_flags["animator"] = EntityAnimator(player, "state_attack")
        if "move" in events:
            if "animator" in player.render_flags:
                player.render_flags["animator"].set_animation("state_walk", 500, 0)
            else:
                player.render_flags["animator"] = EntityAnimator(player, "state_walk", 500, 0)
        if "plant_request" in events:
            if "animator" in player.render_flags:
                player.render_flags["animator"].set_animation("state_plant")
            else:
                player.render_flags["animator"] = EntityAnimator(player, "state_plant")

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

        if "death" in events:
            if "animator" in carrot.render_flags:
                carrot.render_flags["animator"].set_animation("state_die")
            else:
                carrot.render_flags["animator"] = EntityAnimator(carrot, "state_die")
        if "attack" in events:
            if "animator" in carrot.render_flags:
                carrot.render_flags["animator"].set_animation("state_attack")
            else:
                carrot.render_flags["animator"] = EntityAnimator(carrot, "state_attack")
        if "move" in events:
            if "animator" in carrot.render_flags:
                carrot.render_flags["animator"].set_animation("state_walk", 500, 0)
            else:
                carrot.render_flags["animator"] = EntityAnimator(carrot, "state_walk", 500, 0)

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
        
    def render_sprout(self, sprout:Sprout):
        events = []
        for e in sprout.events:
            if e["name"] == "death":
                events.append("death")
            elif e["name"] == "attack":
                events.append("attack")
            elif e["name"] == "move":
                events.append("move")

        if "death" in events:
            if "animator" in sprout.render_flags:
                sprout.render_flags["animator"].set_animation("state_die")
            else:
                sprout.render_flags["animator"] = EntityAnimator(sprout, "state_die")
        if "attack" in events:
            if "animator" in sprout.render_flags:
                sprout.render_flags["animator"].set_animation("state_attack")
            else:
                sprout.render_flags["animator"] = EntityAnimator(sprout, "state_attack")
        if "move" in events:
            if "animator" in sprout.render_flags:
                sprout.render_flags["animator"].set_animation("state_walk", 500, 0)
            else:
                sprout.render_flags["animator"] = EntityAnimator(sprout, "state_walk", 500, 0)

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
            

