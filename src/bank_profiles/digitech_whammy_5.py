# DigiTech Whammy 5

# Docs: https://digitech.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dw18aa3ac1/pdfs/Whammy_OM_EN.pdf

# Set MIDI Channel on the board
# The Whammy can receive MIDI messages on any, or all MIDI channels. The following steps outline
# the procedure for accessing or changing the MIDI channel.
# 1. Disconnect the power from the Whammy pedal.
# 2. Press and hold the Effect On/Off Footswitch while reconnecting the power. One of the
#    Effect LEDs will begin to flash indicating the currently selected MIDI channel.
# 3. Using the reference chart below, rotate the Selector Knob to select the desired MIDI
#    channel.
# 4. Press the Effect On/Off Footswitch again to exit the MIDI set up menu.

# Channel 1: Up 2 Oct
# Channel 2: Up Oct
# Channel 3: Up 5th
# Channel 4: Up 4th
# Channel 5: Down 2nd
# Channel 6: Down 4th
# Channel 7: Down 5th
# Channel 8: Down Oct
# Channel 9: Down 2 Oct
# Channel 10: Dive Bomb
# Channel 11: Deep
# Channel 12: Shallow
# Channel 13: Up 2nd 3rd
# Channel 14: Up b3rd 3rd
# Channel 15: Up 3rd 4th
# Channel 16: Up 4th 5th
# Omni (any): Up 5th 6th

# Calibrating the Expression Pedal
# In the unlikely event that the Expression Pedal does not respond properly or that the note does
# not bend or return to the correct pitch, it may need to be re-calibrated. The following steps outline
# the procedure for Expression Pedal re-calibration:
# 1. Disconnect the power from the Whammy pedal.
# 2. Press and hold the WHAMMY Effect Footswitch while reconnecting the power. This
#    enables MIDI and Calibration Setup. Wait for one of the WHAMMY Effect LEDs to
#    begin flashing (indicating the currently selected MIDI channel) then release the footswitch.
# 3. Rock the Expression Pedal fully forward (toe down) and fully back (toe up) at least two
#    times. The 4 HARMONY LEDs will light back and forth (from 5TH UP/7TH UP to OCT
#    DN/OCT UP) as the pedal is rocked indicating the pedal is calibrating.
# 4. When finished, press the WHAMMY Effect Footswi

# MIDI Program Changes
# (the value must be one less than the value specified in the documentation)
PC_CLASSIC_UP_2_OCT_ACTIVE = 0
PC_CLASSIC_UP_OCT_ACTIVE = 1
PC_CLASSIC_UP_5TH_ACTIVE = 2
PC_CLASSIC_UP_4TH_ACTIVE = 3
PC_CLASSIC_DOWN_2ND_ACTIVE = 4
PC_CLASSIC_DOWN_4TH_ACTIVE = 5
PC_CLASSIC_DOWN_5TH_ACTIVE = 6
PC_CLASSIC_DOWN_OCT_ACTIVE = 7
PC_CLASSIC_DOWN_2_OCT_ACTIVE = 8
PC_CLASSIC_DIVE_BOMB_ACTIVE = 9
PC_CLASSIC_DEEP_ACTIVE = 10
PC_CLASSIC_SHALLOW_ACTIVE = 11
PC_CLASSIC_UP_2ND_3RD_ACTIVE = 12
PC_CLASSIC_UP_b3RD_3RD_ACTIVE = 13
PC_CLASSIC_UP_3RD_4TH_ACTIVE = 14
PC_CLASSIC_UP_4TH_5TH_ACTIVE = 15
PC_CLASSIC_UP_5TH_6TH_ACTIVE = 16
PC_CLASSIC_UP_5TH_7TH_ACTIVE = 17
PC_CLASSIC_DOWN_4TH_3RD_ACTIVE = 18
PC_CLASSIC_DOWN_5TH_4TH_ACTIVE = 19
PC_CLASSIC_DOWN_UP_OCT_ACTIVE = 20

PC_CLASSIC_UP_2_OCT_BYPASS = 21
PC_CLASSIC_UP_OCT_BYPASS = 22
PC_CLASSIC_UP_5TH_BYPASS = 23
PC_CLASSIC_UP_4TH_BYPASS = 24
PC_CLASSIC_DOWN_2ND_BYPASS = 25
PC_CLASSIC_DOWN_4TH_BYPASS = 26
PC_CLASSIC_DOWN_5TH_BYPASS = 27
PC_CLASSIC_DOWN_OCT_BYPASS = 28
PC_CLASSIC_DOWN_2_OCT_BYPASS = 29
PC_CLASSIC_DIVE_BOMB_BYPASS = 30
PC_CLASSIC_DEEP_BYPASS = 31
PC_CLASSIC_SHALLOW_BYPASS = 32
PC_CLASSIC_UP_2ND_3RD_BYPASS = 33
PC_CLASSIC_UP_b3RD_3RD_BYPASS = 34
PC_CLASSIC_UP_3RD_4TH_BYPASS = 35
PC_CLASSIC_UP_4TH_5TH_BYPASS = 36
PC_CLASSIC_UP_5TH_6TH_BYPASS = 37
PC_CLASSIC_UP_5TH_7TH_BYPASS = 38
PC_CLASSIC_DOWN_4TH_3RD_BYPASS = 39
PC_CLASSIC_DOWN_5TH_4TH_BYPASS = 40
PC_CLASSIC_DOWN_UP_OCT_BYPASS = 41

PC_CHORDS_UP_2_OCT_ACTIVE = 42
PC_CHORDS_UP_OCT_ACTIVE = 43
PC_CHORDS_UP_5TH_ACTIVE = 44
PC_CHORDS_UP_4TH_ACTIVE = 45
PC_CHORDS_DOWN_2ND_ACTIVE = 46
PC_CHORDS_DOWN_4TH_ACTIVE = 47
PC_CHORDS_DOWN_5TH_ACTIVE = 48
PC_CHORDS_DOWN_OCT_ACTIVE = 49
PC_CHORDS_DOWN_2_OCT_ACTIVE = 50
PC_CHORDS_DIVE_BOMB_ACTIVE = 51
PC_CHORDS_DEEP_ACTIVE = 52
PC_CHORDS_SHALLOW_ACTIVE = 53
PC_CHORDS_UP_2ND_3RD_ACTIVE = 54
PC_CHORDS_UP_b3RD_3RD_ACTIVE = 55
PC_CHORDS_UP_3RD_4TH_ACTIVE = 56
PC_CHORDS_UP_4TH_5TH_ACTIVE = 57
PC_CHORDS_UP_5TH_6TH_ACTIVE = 58
PC_CHORDS_UP_5TH_7TH_ACTIVE = 59
PC_CHORDS_DOWN_4TH_3RD_ACTIVE = 60
PC_CHORDS_DOWN_5TH_4TH_ACTIVE = 61
PC_CHORDS_DOWN_UP_OCT_ACTIVE = 62

PC_CHORDS_UP_2_OCT_BYPASS = 63
PC_CHORDS_UP_OCT_BYPASS = 64
PC_CHORDS_UP_5TH_BYPASS = 65
PC_CHORDS_UP_4TH_BYPASS = 66
PC_CHORDS_DOWN_2ND_BYPASS = 67
PC_CHORDS_DOWN_4TH_BYPASS = 68
PC_CHORDS_DOWN_5TH_BYPASS = 69
PC_CHORDS_DOWN_OCT_BYPASS = 70
PC_CHORDS_DOWN_2_OCT_BYPASS = 71
PC_CHORDS_DIVE_BOMB_BYPASS = 72
PC_CHORDS_DEEP_BYPASS = 73
PC_CHORDS_SHALLOW_BYPASS = 74
PC_CHORDS_UP_2ND_3RD_BYPASS = 75
PC_CHORDS_UP_b3RD_3RD_BYPASS = 76
PC_CHORDS_UP_3RD_4TH_BYPASS = 77
PC_CHORDS_UP_4TH_5TH_BYPASS = 78
PC_CHORDS_UP_5TH_6TH_BYPASS = 79
PC_CHORDS_UP_5TH_7TH_BYPASS = 80
PC_CHORDS_DOWN_4TH_3RD_BYPASS = 81
PC_CHORDS_DOWN_5TH_4TH_BYPASS = 82
PC_CHORDS_DOWN_UP_OCT_BYPASS = 83

# MIDI Continuous Control Change
CC_EXPRESSION_NUM = 11
CC_EXPRESSION_VAL_MIN = 0  # toe up position
CC_EXPRESSION_VAL_MAX = 127  # toe down position

# !!! not tested
CC_EFFECT_SWITCH_NUM = 0
CC_EFFECT_SWITCH_ON_VAL = 127
CC_EFFECT_SWITCH_OFF_VAL = 0

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
    "META:NAME": "ALL (global state)",
    "ON:ENTER": [
        {
            "FUNC": "LED:BLINK",
            "ARGS": {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 1, "fps": 50},
        },
        {"FUNC": "STATE:RESET", "ARGS": {"id": "ACA"}},
        {"FUNC": "MIDI:PC", "ARGS": {"num": 1}},
        LED_YELLOW_CMD,
    ],
    "ON:EXIT": [],
    "BTN:A": {
        "ON:PRESS": [
            {"CMD": [{"FUNC": "STATE:CALL_PREV", "ARGS": {"id": "ACA"}}]},
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            {"CMD": [{"FUNC": "STATE:CALL_NEXT", "ARGS": {"id": "ACA"}}]},
        ],
    },
    "COMB:A+B": {
        "ON:PRESS": [
            {"CMD": [NEXT_BOARD_BANK_CMD]},
        ],
    },
}

BANK_2 = {
    "META:NAME": "All",
    "ON:ENTER": [
        {
            "FUNC": "LED:BLINK",
            "ARGS": {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 2, "fps": 50},
        },
        LED_GREEN_CMD,
    ],
    "ON:EXIT": [],
    "BTN:A": {
        "ON:PRESS": [
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_2_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_5TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_4TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_2ND_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_4TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_5TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_2_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DIVE_BOMB_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DEEP_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_SHALLOW_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_2ND_3RD_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_b3RD_3RD_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_3RD_4TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_4TH_5TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_5TH_6TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_5TH_7TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_4TH_3RD_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_5TH_4TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_UP_OCT_ACTIVE}}]},
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_2_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_5TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_4TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_2ND_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_4TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_5TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_2_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DIVE_BOMB_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DEEP_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_SHALLOW_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_2ND_3RD_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_b3RD_3RD_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_3RD_4TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_4TH_5TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_5TH_6TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_5TH_7TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_4TH_3RD_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_5TH_4TH_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_UP_OCT_ACTIVE}}]},
        ],
    },
    "COMB:A+B": {
        "ON:PRESS": [
            {"CMD": [NEXT_BOARD_BANK_CMD]},
        ],
    },
}

BANK_3 = {
    "META:NAME": "Favorites Classic",
    "ON:ENTER": [
        {
            "FUNC": "LED:BLINK",
            "ARGS": {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 3, "fps": 50},
        },
        LED_BLUE_CMD,
    ],
    "ON:EXIT": [],
    "BTN:A": {
        "ON:PRESS": [
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_SHALLOW_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_2ND_3RD_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_UP_OCT_ACTIVE}}]},
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_OCT_ACTIVE}}]},
        ],
    },
    "COMB:A+B": {
        "ON:PRESS": [
            {"CMD": [NEXT_BOARD_BANK_CMD]},
        ],
    },
}

BANK_4 = {
    "META:NAME": "Favorites Chords",
    "ON:ENTER": [
        {
            "FUNC": "LED:BLINK",
            "ARGS": {"id": "SYS", "on_time": 0, "fade_in_time": 0.15, "off_time": 0, "n": 4, "fps": 50},
        },
        LED_RED_CMD,
    ],
    "ON:EXIT": [],
    "BTN:A": {
        "ON:PRESS": [
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_SHALLOW_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_2ND_3RD_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_UP_OCT_ACTIVE}}]},
        ],
    },
    "BTN:B": {
        "ON:PRESS": [
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_UP_OCT_ACTIVE}}]},
            {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CHORDS_DOWN_OCT_ACTIVE}}]},
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
        "ACA": {
            "NAME": "All Classic Active",
            "VARS": {},
            "STATES": [
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_2_OCT_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_OCT_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_5TH_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_4TH_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_2ND_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_4TH_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_5TH_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_OCT_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_2_OCT_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DIVE_BOMB_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DEEP_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_SHALLOW_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_2ND_3RD_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_b3RD_3RD_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_3RD_4TH_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_4TH_5TH_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_5TH_6TH_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_UP_5TH_7TH_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_4TH_3RD_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_5TH_4TH_ACTIVE}}]},
                {"CMD": [{"FUNC": "MIDI:PC", "ARGS": {"num": PC_CLASSIC_DOWN_UP_OCT_ACTIVE}}]},
            ],
        },
    },
    "BANKS": [
        BANK_1,
        BANK_2,
        BANK_3,
        BANK_4,
    ],
}
