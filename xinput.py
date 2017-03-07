import ctypes
from enum import Enum
from time import sleep
from time import time as time_now

# XINPUT ACCESS #
# Constants
NOT_CONNECTED = 1167
UBYTE = 255
CSHORT = 32767
USHORT = 65535


# Structures
class XINPUTGAMEPAD(ctypes.Structure):
    _fields_ = [("wButtons", ctypes.c_ushort),
                ("bLeftTrigger", ctypes.c_ubyte),
                ("bRightTrigger", ctypes.c_ubyte),
                ("sThumbLX", ctypes.c_short),
                ("sThumbLY", ctypes.c_short),
                ("sThumbRX", ctypes.c_short),
                ("sThumbRY", ctypes.c_short)]


class XINPUTSTATE(ctypes.Structure):
    _fields_ = [("dwPacketNumber", ctypes.c_uint32),
                ("Gamepad", XINPUTGAMEPAD)]


class XINPUTVIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

# load Xinput.dll
try:
    _xinput = ctypes.windll.xinput9_1_0
except:
    raise ImportError

# getState
_XInputGetState = _xinput.XInputGetState
_XInputGetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUTSTATE)]
_XInputGetState.resttype = ctypes.c_uint
# setVibration
_XInputSetState = _xinput.XInputSetState
_XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUTVIBRATION)]
_XInputSetState.restype = ctypes.c_uint


class AnalogStick:
    def __init__(self, raw_x, raw_y, deadzone):
        self.raw_x = raw_x
        self.raw_y = raw_y
        axis_x = raw_x / CSHORT
        axis_y = raw_y / CSHORT
        magnitude = (axis_x ** 2 + axis_y ** 2) ** 0.5
        if magnitude > deadzone:
            dz_factor = (magnitude - deadzone) / (1 - deadzone)
            self.x = axis_x / magnitude * dz_factor
            self.y = axis_y / magnitude * dz_factor
            self.magnitude = magnitude
        else:
            self.x = 0
            self.y = 0
            self.magnitude = 0


class Gamepad(Enum):
    gamepad_0 = 0
    gamepad_1 = 1
    gamepad_2 = 2
    gamepad_3 = 3

    @staticmethod
    def update():
        t_now = time_now()
        state = XINPUTSTATE()
        for gamepad in Gamepad:
            if not gamepad.disabled:
                if gamepad.connected:
                    gamepad.get_state(state)
                elif t_now - gamepad.last_update > 5:
                    print("XGamepad checking up on {}".format(gamepad))
                    gamepad.get_state(state)

    def __init__(self, value):
        # hardware info
        self._raw_id = value
        self.disabled = False
        self.connected = False
        self.deadzone = 0.3
        self.last_update = 0
        self.input_state = None
        self._reset_input()
        # vibration
        self.vibration_left = 0
        self.vibration_right = 0

    def __repr__(self):
        return "XGamepad:gamepad{}".format(self._raw_id)

    def __str__(self):
        if self.connected:
            tmp = "connected"
        else:
            tmp = "not connected"
        return "gamepad{}({})".format(self._raw_id, tmp)

    def _reset_input(self):
        self.input_state = {
            "analog_right": AnalogStick(0, 0, self.deadzone),
            "analog_left": AnalogStick(0, 0, self.deadzone),
            "trigger_right": 0,
            "trigger_left": 0,
            "shoulder_right": False,
            "shoulder_left": False,
            "button_start": False,
            "button_back": False,
            "stick_right": False,
            "stick_left": False,
            "button_a": False,
            "button_b": False,
            "button_x": False,
            "button_y": False,
            "dpad_right": False,
            "dpad_left": False,
            "dpad_down": False,
            "dpad_up": False,
            "events": None
        }

    def set_vibration(self, left: float=0, right: float=0):
        self.vibration_left = left
        self.vibration_right = right
        vibration = XINPUTVIBRATION(int(left * USHORT), int(right * USHORT))
        _XInputSetState(self._raw_id, ctypes.byref(vibration))

    def get_state(self, state=None):
        if not state:
            state = XINPUTSTATE()
        self.last_update = time_now()
        error_code = _XInputGetState(self._raw_id, state)
        if error_code == NOT_CONNECTED:
            if self.connected:
                # update connection status
                self.connected = False
                # reset input fields
                self._reset_input()
                # disconnected!
                print(self)
            # update connection status
            self.connected = False
        else:
            if not self.connected:
                # update connection status
                self.connected = True
                # deactivate vibration
                self.set_vibration()
                # reconnected!
                print(self)
            # update state and stats
            self.connected = True
            gamepad = state.Gamepad
            new_state = dict()
            events = dict()
            # analog_right
            new_value = AnalogStick(gamepad.sThumbRX, gamepad.sThumbRY, self.deadzone)
            old_value = self.input_state["analog_right"]
            dx = new_value.x - old_value.x
            dy = new_value.y - old_value.y
            if abs(dx) > 0 or abs(dy) > 0:
                events["analog_right"] = (dx, dy)
            new_state["analog_right"] = new_value
            # analog_left
            new_value = AnalogStick(gamepad.sThumbLX, gamepad.sThumbLY, self.deadzone)
            old_value = self.input_state["analog_left"]
            dx = new_value.x - old_value.x
            dy = new_value.y - old_value.y
            if abs(dx) > 0 or abs(dy) > 0:
                events["analog_left"] = (dx, dy)
            new_state["analog_left"] = new_value
            # trigger_right
            new_value = gamepad.bRightTrigger/UBYTE
            old_value = self.input_state["trigger_right"]
            delta = new_value - old_value
            if abs(delta) > 0:
                events["trigger_right"] = delta
            new_state["trigger_right"] = new_value
            # trigger_left
            new_value = gamepad.bLeftTrigger/UBYTE
            old_value = self.input_state["trigger_left"]
            delta = new_value - old_value
            if abs(delta) > 0:
                events["trigger_left"] = delta
            new_state["trigger_left"] = new_value

            def get_button(mask):
                return gamepad.wButtons & mask is not 0
            # dpad_up
            new_value = get_button(0x0001)
            old_value = self.input_state["dpad_up"]
            if new_value and not old_value:
                events["dpad_up"] = True
            elif old_value and not new_value:
                events["dpad_up"] = False
            new_state["dpad_up"] = new_value
            # dpad_down
            new_value = get_button(0x0002)
            old_value = self.input_state["dpad_down"]
            if new_value and not old_value:
                events["dpad_down"] = True
            elif old_value and not new_value:
                events["dpad_down"] = False
            new_state["dpad_down"] = new_value
            # dpad_left
            new_value = get_button(0x0004)
            old_value = self.input_state["dpad_left"]
            if new_value and not old_value:
                events["dpad_left"] = True
            elif old_value and not new_value:
                events["dpad_left"] = False
            new_state["dpad_left"] = new_value
            # dpad_right
            new_value = get_button(0x0008)
            old_value = self.input_state["dpad_right"]
            if new_value and not old_value:
                events["dpad_right"] = True
            elif old_value and not new_value:
                events["dpad_right"] = False
            new_state["dpad_right"] = new_value
            # button_start
            new_value = get_button(0x0010)
            old_value = self.input_state["button_start"]
            if new_value and not old_value:
                events["button_start"] = True
            elif old_value and not new_value:
                events["button_start"] = False
            new_state["button_start"] = new_value
            # button_back
            new_value = get_button(0x0020)
            old_value = self.input_state["button_back"]
            if new_value and not old_value:
                events["button_back"] = True
            elif old_value and not new_value:
                events["button_back"] = False
            new_state["button_back"] = new_value
            # stick_left
            new_value = get_button(0x0040)
            old_value = self.input_state["stick_left"]
            if new_value and not old_value:
                events["stick_left"] = True
            elif old_value and not new_value:
                events["stick_left"] = False
            new_state["stick_left"] = new_value
            # stick_right
            new_value = get_button(0x0080)
            old_value = self.input_state["stick_right"]
            if new_value and not old_value:
                events["stick_right"] = True
            elif old_value and not new_value:
                events["stick_right"] = False
            new_state["stick_right"] = new_value
            # shoulder_left
            new_value = get_button(0x0100)
            old_value = self.input_state["shoulder_left"]
            if new_value and not old_value:
                events["shoulder_left"] = True
            elif old_value and not new_value:
                events["shoulder_left"] = False
            new_state["shoulder_left"] = new_value
            # shoulder_right
            new_value = get_button(0x0200)
            old_value = self.input_state["shoulder_right"]
            if new_value and not old_value:
                events["shoulder_right"] = True
            elif old_value and not new_value:
                events["shoulder_right"] = False
            new_state["shoulder_right"] = new_value
            # button_a
            new_value = get_button(0x1000)
            old_value = self.input_state["button_a"]
            if new_value and not old_value:
                events["button_a"] = True
            elif old_value and not new_value:
                events["button_a"] = False
            new_state["button_a"] = new_value
            # button_b
            new_value = get_button(0x2000)
            old_value = self.input_state["button_b"]
            if new_value and not old_value:
                events["button_b"] = True
            elif old_value and not new_value:
                events["button_b"] = False
            new_state["button_b"] = new_value
            # button_x
            new_value = get_button(0x4000)
            old_value = self.input_state["button_x"]
            if new_value and not old_value:
                events["button_x"] = True
            elif old_value and not new_value:
                events["button_x"] = False
            new_state["button_x"] = new_value
            # button_y
            new_value = get_button(0x8000)
            old_value = self.input_state["button_y"]
            if new_value and not old_value:
                events["button_y"] = True
            elif old_value and not new_value:
                events["button_y"] = False
            new_state["button_y"] = new_value
            # inauguration
            new_state["event"] = events
            self.input_state = new_state
