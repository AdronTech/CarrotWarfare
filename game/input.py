from game.commands import Commands
from xinput import Gamepad
from pygame.math import Vector2
from pygame import event as pygame_events
from pygame import *

key_board_enabled = True
key_board_player = -1


def get_input(pygame_events):
    Gamepad.update()
    gamepads = list(Gamepad)
    commands = [[], [], [], []]
    for i in range(len(gamepads)):

        if i is key_board_player:
            #
            # if mouse.get_focused():
            #     mouse.set_pos(200, 200)
            #     mouse.set_visible(False)

            move_dir = Vector2()
            look_dir = Vector2()

            for e in pygame_events:
                print(e)

                if e.type is KEYDOWN:
                    if e.key is K_SPACE:
                        commands[i].append({"command": Commands.swap})

                elif e.type is MOUSEBUTTONDOWN:
                    if e.button is 1:
                        commands[i].append({"command": Commands.call})
                    elif e.button is 2:
                        commands[i].append({"command": Commands.plant})
                    elif e.button is 3:
                        commands[i].append({"command": Commands.attack})

                elif e.type is MOUSEMOTION:
                    look_dir = -Vector2(e.rel)

            pressed = key.get_pressed()

            if pressed[K_w]:
                move_dir += Vector2(0, -1)

            if pressed[K_a]:
                move_dir += Vector2(-1, 0)

            if pressed[K_s]:
                move_dir += Vector2(0, 1)

            if pressed[K_d]:
                move_dir += Vector2(1, 0)

            if move_dir.x != 0 or move_dir.y != 0:
                move_dir.normalize_ip()

                commands[i].append({
                    "command": Commands.directional,
                    "dir": move_dir
                })

            look_dir = move_dir

            if look_dir.x != 0 or look_dir.y != 0:
                look_dir.normalize_ip()

                commands[i].append({
                    "command": Commands.look,
                    "dir": look_dir
                })

        elif gamepads[i].connected:
            x = gamepads[i].input_state["analog_left"].x
            y = gamepads[i].input_state["analog_left"].y
            if x != 0 or y != 0:

                dir = Vector2(x, -y)

                if gamepads[i].input_state["trigger_right"] < 0.5:
                    commands[i].append({
                        "command": Commands.directional,
                        "dir": dir
                    })

                commands[i].append({
                    "command": Commands.look,
                    "dir": dir
                })

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
    players = []
    for i in range(len(gamepads)):
        if gamepads[i].connected:
            players.append(i)
        else:
            global key_board_player
            if key_board_enabled and key_board_player is -1:
                key_board_player = i
                players.append(i)

            gamepads[i].disabled = True

    return players
