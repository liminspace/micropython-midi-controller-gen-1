# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Any, Dict, List

PROFILE_PATH = "bank_profiles.line6_hx_stomp.profile_1"
# PROFILE_PATH = "bank_profiles.digitech_whammy_5.profile_1"


DEBUG: bool = False
IGNORE_COMMAND_ERRORS: bool = False

BOARD_BUTTONS: Dict[str, Dict[str, Any]] = {
    "A": {
        "port": 15,
    },
    "B": {
        "port": 14,
    },
    #     'C': {
    #         'port': 13,
    #     },
    #     'D': {
    #         'port': 12,
    #     },
    #     'E': {
    #         'port': 11,
    #     },
    #     'F': {
    #         'port': 10,
    #     },
}

BOARD_LEDS: Dict[str, Dict[str, Any]] = {
    "SYS": {
        "port": 25,
        "active_high": True,  # if pin connected to anode(+) use True; if to cathode(-) use False; default True
        "pwm": True,  # set True to support dynamic brightness; default True
        "initial_value": False,  # ON = True; OFF = False; or 0.0...1..0; default False
        "reset_skip": True,  # don't turn off when bank is changed
    },
}

BOARD_RGB_LEDS: Dict[str, Dict[str, Any]] = {
    "1": {
        "port_red": 16,
        "port_green": 17,
        "port_blue": 18,
        "active_high": False,  # if led has common cathode(-) use True; if common anode(+) use False; default True
        "pwm": True,  # set True to support dynamic brightness; default True
        "initial_value": (0.0, 0.0, 0.0, 0.1),  # RGB+brightness 0.0...1.0; default (0, 0, 0, 1)
    },
}

# ADC ports only
BOARD_POTS: Dict[str, Dict[str, Any]] = {
    #     '1': {
    #         'port': 26,
    #         'active_state': True,  # default True
    #         'threshold': 0.5,  # default 0.5
    #     },
    #     '2': {
    #         'port': 27,
    #         'active_state': True,  # default True
    #         'threshold': 0.5,  # default 0.5
    #
    #     },
    #     '3': {
    #         'port': 28,
    #         'active_state': True,  # default True
    #         'threshold': 0.5,  # default 0.5
    #     },
}

# UART TX ports only
BOARD_OUT_MIDIS: Dict[str, Dict[str, Any]] = {
    "1": {
        "uart": 1,
        "port": 8,
        "default_channel": 1,  # can be None
        "is_default": True,
    },
}

COMMANDS_ON_BOOT: List[Dict] = [  #
    # list of commands like in banks' files
    # will be performed only after success init
    # {"FUNC": "LED:ON", "ARGS": {"id": "SYS"}},
    # {"FUNC": "TIME:SLEEP", "ARGS": {"value": 500}},
    {
        "FUNC": "LED:BLINK",
        "ARGS": {"id": "SYS", "on_time": 0, "fade_in_time": 0.2, "off_time": 0, "n": 1, "fps": 50},
    },
    # {"FUNC": "TIME:SLEEP", "ARGS": {"val": 1000}},
    # {"FUNC": "LED:OFF", "ARGS": {"id": "SYS"}},
    # {"FUNC": "RGB_LED:COLOR", "ARGS": {"id": "1", "val": (255, 0, 0, 0.1)}},
    # {"FUNC": "MIDI:CC", "ARGS": {"num": 69, "val": 8}},
    # {"FUNC": "TIME:SLEEP", "ARGS": {"val": 300}},
    # {"FUNC": "RGB_LED:COLOR", "ARGS": {"id": "1", "val": (0, 255, 0, 0.1)}},
    # {"FUNC": "MIDI:CC", "ARGS": {"num": 69, "val": 8}},
    # {"FUNC": "TIME:SLEEP", "ARGS": {"val": 300}},
    # {"FUNC": "RGB_LED:COLOR", "ARGS": {"id": "1", "val": (0, 0, 255, 0.1)}},
    # {"FUNC": "MIDI:CC", "ARGS": {"num": 69, "val": 8}},
    # {"FUNC": "TIME:SLEEP", "ARGS": {"val": 300}},
]
