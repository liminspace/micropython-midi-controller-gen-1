# LINE6 HX STOMP

next_snapshot = ("next snapshot", "MIDI:CC", {"num": 69, "val": 8})
prev_snapshot = ("prev snapshot", "MIDI:CC", {"num": 69, "val": 9})

next_board_bank = ("next board bank", "BANK:NEXT", {})

led_red = ("led red", "RGB_LED:COLOR", {"id": "1", "val": (255, 0, 0, 0.07)})
led_green = ("led green", "RGB_LED:COLOR", {"id": "1", "val": (0, 255, 0, 0.07)})
led_blue = ("led blue", "RGB_LED:COLOR", {"id": "1", "val": (0, 0, 255, 0.08)})
led_yellow = ("led yellow", "RGB_LED:COLOR", {"id": "1", "val": (255, 255, 0, 0.07)})
led_magenta = ("led magenta", "RGB_LED:COLOR", {"id": "1", "val": (255, 0, 255, 0.07)})
led_cyan = ("led cyan", "RGB_LED:COLOR", {"id": "1", "val": (0, 255, 255, 0.07)})
led_white = ("led cyan", "RGB_LED:COLOR", {"id": "1", "val": (255, 255, 255, 0.05)})

bank_1 = {
    "ATTR:NAME": "BANK_1",
    "ON:ENTER": [
        led_green,
    ],
    "ON:EXIT": [
        (
            "",
            "LED:BLINK",
            {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 2, "fps": 50},
        )
    ],
    "BTN:A": {
        "ON:PRESS": [
            (
                "prev snapshot",
                [
                    prev_snapshot,
                ],
            ),
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            (
                "next snapshot",
                [
                    next_snapshot,
                ],
            ),
        ],
    },
    "COMB:A+B": {
        "ON:PRESS": [
            (
                "next board bank",
                [
                    next_board_bank,
                ],
            ),
        ],
    },
}

bank_2 = {
    "ATTR:NAME": "BANK_2",
    "ON:ENTER": [
        led_blue,
    ],
    "ON:EXIT": [
        (
            "",
            "LED:BLINK",
            {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 3, "fps": 50},
        ),
    ],
    "BTN:A": {
        "ON:PRESS": [
            (
                "next snapshot",
                [
                    next_snapshot,
                ],
            ),
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            (
                "prev shanpshot",
                [
                    prev_snapshot,
                ],
            ),
            (
                "prev shanpshot",
                [
                    prev_snapshot,
                ],
            ),
        ],
    },
    "COMB:A+B": {
        "ON:PRESS": [
            (
                "next board bank",
                [
                    next_board_bank,
                ],
            ),
        ],
    },
}

bank_3 = {
    "ATTR:NAME": "BANK_3",
    "ON:ENTER": [
        led_red,
    ],
    "ON:EXIT": [
        (
            "",
            "LED:BLINK",
            {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 1, "fps": 50},
        ),
    ],
    "BTN:A": {
        "ON:PRESS": [
            (
                "programs",
                [
                    ("DIR:Glossary", "MIDI:PC", {"num": 63}),
                ],
            ),
            (
                "programs",
                [
                    ("DIR:Pop My Punk", "MIDI:PC", {"num": 64}),
                ],
            ),
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            (
                "programs",
                [
                    ("DIR:Goth or Mod?", "MIDI:PC", {"num": 69}),
                ],
            ),
            (
                "programs",
                [
                    ("KEY:Gritz", "MIDI:PC", {"num": 94}),
                ],
            ),
        ],
    },
    "COMB:A+B": {
        "ON:PRESS": [
            (
                "next board bank",
                [
                    next_board_bank,
                ],
            ),
        ],
    },
}

default_profile = {
    "global_states": {},
    "banks": [
        bank_1,
        bank_2,
        bank_3,
    ],
}
