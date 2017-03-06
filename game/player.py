import game.entity


def get_player():
    player = game.entity.Entity()
    player.type = "player"
    player.dump = {"input": [], "seed_mode": "melee"}
    player.update = player_update
    return player


def player_update(self):
    input_commands = self.dump.get("input")
    for c in input_commands:
        command = c[0]
        if command == "directional":
            # de-register player in old tile
            # add (c[1], c[2]) onto pos (mind border collision)
            # register player in new tile
            pass
        elif command == "attack":
            # cast attack on current position
            pass
        elif command == "plant":
            # if seed available: plant player-colored seed on current tile (mind seed_mode?)
            pass
        elif command == "call":
            # trigger homing of player's carrots
            pass
        elif command == "swap":
            # swap player's seed_mode
            pass
