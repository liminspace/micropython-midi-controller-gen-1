# LINE6 HX STOMP

SNAPSHOT_1_CMD = {"NAME": "Snapshot 1", "FUNC": "MIDI:CC", "ARGS": {"num": 69, "val": 0}}
SNAPSHOT_2_CMD = {"NAME": "Snapshot 2", "FUNC": "MIDI:CC", "ARGS": {"num": 69, "val": 1}}
SNAPSHOT_3_CMD = {"NAME": "Snapshot 3", "FUNC": "MIDI:CC", "ARGS": {"num": 69, "val": 2}}

SNAPSHOT_NEXT_CMD = {"NAME": "Next Snapshot", "FUNC": "MIDI:CC", "ARGS": {"num": 69, "val": 8}}
SNAPSHOT_PREV_CMD = {"NAME": "Prev Snapshot", "FUNC": "MIDI:CC", "ARGS": {"num": 69, "val": 9}}

NEXT_BOARD_BANK_CMD = {"NAME": "Next Board Bank", "FUNC": "BANK:NEXT"}

LED_RED_CMD = {"NAME": "LED Red", "FUNC": "RGB_LED:COLOR", "ARGS": {"id": "1", "val": (255, 0, 0, 0.07)}}
LED_GREEN_CMD = {
    "NAME": "LED Green",
    "FUNC": "RGB_LED:COLOR",
    "ARGS": {"id": "1", "val": (0, 255, 0, 0.07)},
}
LED_BLUE_CMD = {"NAME": "LED Blue", "FUNC": "RGB_LED:COLOR", "ARGS": {"id": "1", "val": (0, 0, 255, 0.08)}}
LED_YELLOW_CMD = {
    "NAME": "LED Yellow",
    "FUNC": "RGB_LED:COLOR",
    "ARGS": {"id": "1", "val": (255, 255, 0, 0.07)},
}
LED_MAGENTA_CMD = {
    "NAME": "LED Magenta",
    "FUNC": "RGB_LED:COLOR",
    "ARGS": {"id": "1", "val": (255, 0, 255, 0.07)},
}
LED_CYAN_CMD = {
    "NAME": "LED Cyan",
    "FUNC": "RGB_LED:COLOR",
    "ARGS": {"id": "1", "val": (0, 255, 255, 0.07)},
}
LED_WHITE_CMD = {
    "NAME": "LED White",
    "FUNC": "RGB_LED:COLOR",
    "ARGS": {"id": "1", "val": (255, 255, 255, 0.05)},
}

BANK_1 = {
    "META:NAME": "BANK 1",
    "ON:ENTER": [
        # commands
        {
            "FUNC": "LED:BLINK",
            "ARGS": {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 1, "fps": 50},
        },
        {
            "FUNC": "STATE:RESET",
            "ARGS": {"id": "FS"},
        },
        LED_GREEN_CMD,
    ],
    "ON:EXIT": [
        # commands
    ],
    "BTN:A": {
        "ON:PRESS": [
            # states
            {
                "NAME": "Prev Fav",
                "CMD": [
                    # SNAPSHOT_PREV_CMD,
                    {"FUNC": "STATE:CALL_PREV", "ARGS": {"id": "FS"}},
                ],
            },
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            # states
            {
                "NAME": "Next Fav",
                "CMD": [
                    # SNAPSHOT_NEXT_CMD,
                    {"FUNC": "STATE:CALL_NEXT", "ARGS": {"id": "FS"}},
                ],
            },
        ],
    },
    "COMB:A+B": {
        "ON:PRESS": [
            # states
            {
                "NAME": "Next Board Bank",
                "CMD": [
                    NEXT_BOARD_BANK_CMD,
                ],
            },
        ],
    },
}

BANK_2 = {
    "META:NAME": "BANK 2",
    "ON:ENTER": [
        {
            "FUNC": "LED:BLINK",
            "ARGS": {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 2, "fps": 50},
        },
        LED_BLUE_CMD,
    ],
    "ON:EXIT": [],
    "BTN:A": {
        "ON:PRESS": [
            {"CMD": [SNAPSHOT_PREV_CMD]},
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            {"CMD": [SNAPSHOT_NEXT_CMD]},
        ],
    },
    "COMB:A+B": {
        "ON:PRESS": [
            {"CMD": [NEXT_BOARD_BANK_CMD]},
        ],
    },
}

BANK_3 = {
    "META:NAME": "BANK 3",
    "ON:ENTER": [
        {
            "FUNC": "LED:BLINK",
            "ARGS": {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 3, "fps": 50},
        },
        LED_RED_CMD,
    ],
    "ON:EXIT": [],
    "BTN:A": {
        "ON:PRESS": [
            {"CMD": [{"NAME": "DIR:Glossary", "FUNC": "MIDI:PC", "ARGS": {"num": 63}}]},
            {"CMD": [{"NAME": "DIR:Pop My Punk", "FUNC": "MIDI:PC", "ARGS": {"num": 64}}]},
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            {"CMD": [{"NAME": "DIR:Goth or Mod?", "FUNC": "MIDI:PC", "ARGS": {"num": 69}}]},
            {"CMD": [{"NAME": "KEY:Gritz", "FUNC": "MIDI:PC", "ARGS": {"num": 94}}]},
        ],
    },
    "COMB:A+B": {
        "ON:PRESS": [
            {"CMD": [NEXT_BOARD_BANK_CMD]},
        ],
    },
}

profile_1 = {
    "GLOBAL_STATE_GROUPS": {
        "FS": {
            "NAME": "Favorite Snapshots",
            "VARS": {},
            "STATES": [
                {
                    "ID": "FS1",
                    "NAME": "Favorites 1",
                    "CMD": [
                        LED_RED_CMD,
                        SNAPSHOT_1_CMD,
                    ],
                },
                {
                    "ID": "FS2",
                    "NAME": "Favorites 2",
                    "CMD": [
                        LED_GREEN_CMD,
                        SNAPSHOT_2_CMD,
                    ],
                },
                {
                    "ID": "FS3",
                    "NAME": "Favorites 3",
                    "CMD": [
                        LED_BLUE_CMD,
                        SNAPSHOT_3_CMD,
                    ],
                },
            ],
        },
    },
    "BANKS": [
        BANK_1,
        BANK_2,
        BANK_3,
    ],
}
