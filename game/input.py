from game.commands import Commands
from xinput import Gamepad
from pygame.math import Vector2


def get_input():
    Gamepad.update()
    gamepads = list(Gamepad)
    commands = [[], [], [], []]
    for i in range(len(gamepads)):
        if gamepads[i].connected:
            x = gamepads[i].input_state["analog_left"].x
            y = gamepads[i].input_state["analog_left"].y
            if x != 0 or y != 0:
                commands[i].append({"command": Commands.directional, "value": Vector2(x, -y).normalize()})
            events = gamepads[i].input_state["event"]
            if "button_a" in events and events["button_a"]:
                commands[i].append({"command": Commands.attack})
            if "button_b" in events and events["button_b"]:
                commands[i].append({"command": Commands.plant})
            if "button_x" in events and events["button_x"]:
                commands[i].append({"command": Commands.call})
            if "button_y" in events and events["button_y"]:
                commands[i].append({"command": Commands.swap})
    return commands


def lock_input():
    Gamepad.update()
    gamepads = list(Gamepad)
    player_count = 4
    for i in range(len(gamepads)):
        if not gamepads[i].connected:
            player_count = i
            break
    for i in range(player_count, len(gamepads)):
        gamepads[i].disabled = True
    return player_count
