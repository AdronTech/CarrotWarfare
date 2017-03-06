from game.entity import Entity
from game.commands import Commands
from game.world import WORLD_DIMENSION as DIM
from game.world import World


def get_player():
    player = Entity()
    player.type = "player"
    player.dump = {"input": [], "seed_mode": "melee"}
    player.update_function = player_update
    return player


def player_update(self: Entity):
    input_commands = self.dump.get("input")
    for input_command in input_commands:
        command = input_command[0]
        if command == Commands.directional:
            World.grid[int(self.pos.x)][int(self.pos.y)].unregister(self)
            self.pos += (input_command[1], input_command[2])  # scale input values?
            if self.pos.x > DIM[0]:
                self.pos.x = DIM[0]
            elif self.pos.x < 0:
                self.pos.x = 0
            if self.pos.y > DIM[1]:
                self.pos.y = DIM[1]
            elif self.pos.y < 0:
                self.pos.y = 0
            World.grid[int(self.pos.x)][int(self.pos.y)].register(self)
        elif command == Commands.attack:
            # cast attack on current position
            pass
        elif command == Commands.plant:
            # if seed available: plant player-colored seed on current tile (mind seed_mode?)
            pass
        elif command == Commands.call:
            # trigger homing of player's carrots
            pass
        elif command == Commands.swap:
            # swap player's seed_mode
            pass
