import micropython

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from types import ModuleType
    from typing import Any, Dict, Optional, Set, Tuple, Union

    from picozero import LED, PWMLED, RGBLED, DigitalLED, Pot  # noqa: F401

    from common.buttons import Button, ButtonCombination
    from common.midis import OutMIDI


class Board:
    _debug: bool
    _buttons: Dict[str, Button]
    _button_combinations: Dict[Tuple, ButtonCombination]
    _leds: Dict[str, Union[PWMLED, DigitalLED]]
    _rgb_leds: Dict[str, RGBLED]
    _pots: Dict[str, Pot]
    _out_midis: Dict[str, OutMIDI]
    _out_midi_default: Optional[OutMIDI]
    _reset_skip_set: Set[str]

    def __init__(self, config: ModuleType):
        self._debug = config.DEBUG
        self._reset_skip_set = set()
        self._buttons = self._init_buttons(buttons_config=config.BOARD_BUTTONS)
        self._button_combinations = {}
        self._leds = self._init_leds(leds_config=config.BOARD_LEDS)
        self._rgb_leds = self._init_rgb_leds(rgb_leds_config=config.BOARD_RGB_LEDS)
        self._pots = self._init_pots(pots_config=config.BOARD_POTS)
        self._out_midi_default = None
        self._out_midis = self._init_out_midis(out_midis_config=config.BOARD_OUT_MIDIS)

    @property
    def buttons(self) -> Dict[str, "Button"]:
        return self._buttons

    @property
    def button_combinations(self) -> Dict[Tuple, "ButtonCombination"]:
        return self._button_combinations

    @property
    def leds(self) -> Dict[str, Union["PWMLED", "DigitalLED"]]:
        return self._leds

    @property
    def rgb_leds(self) -> Dict[str, RGBLED]:
        return self._rgb_leds

    @property
    def pots(self) -> Dict[str, Pot]:
        return self._pots

    @property
    def out_midis(self) -> Dict[str, "OutMIDI"]:
        return self._out_midis

    @property
    def out_midi_default(self) -> Optional["OutMIDI"]:
        return self._out_midi_default

    def add_button_combination(self, button_combination: "ButtonCombination") -> None:
        bc_id = button_combination.id
        if bc_id in self._button_combinations:
            raise ValueError(f"Button Combination {bc_id} is duplicated")
        self._button_combinations[bc_id] = button_combination
        return None

    def remove_button_combination(self, button_combination_id: str) -> None:
        button_combination = self._button_combinations.get(button_combination_id, None)
        if not button_combination:
            return None
        button_combination.destroy()
        del self._button_combinations[button_combination_id]
        return None

    @micropython.native
    def reset(self) -> None:
        for button_combination in tuple(self._button_combinations.values()):
            self.remove_button_combination(button_combination_id=button_combination.id)
        for button in self.buttons.values():
            button.reset_handlers()
        for led_id, led in self.leds.items():
            if f"led:{led_id}" not in self._reset_skip_set:
                led.off()
        for rgb_led_id, rgb_led in self.rgb_leds.items():
            if f"rgb_led:{rgb_led_id}" not in self._reset_skip_set:
                rgb_led.off()
        return None

    def _init_buttons(self, buttons_config: Dict[str, Any]) -> Dict[str, "Button"]:
        from common.buttons import Button

        buttons = {}
        for btn_id, btn_config in buttons_config.items():
            buttons[btn_id] = Button(
                button_id=btn_id,
                port=btn_config["port"],
                name=f"BTN_{btn_id}",
                debug=self._debug,
            )
        return buttons

    def _init_leds(self, leds_config: Dict[str, Any]) -> Dict[str, Union["PWMLED", "DigitalLED"]]:  # noqa
        from picozero import LED  # noqa: F811

        leds = {}
        for led_id, led_config in leds_config.items():
            leds[led_id] = LED(
                pin=led_config["port"],
                pwm=led_config.get("pwm", True),
                active_high=led_config.get("active_high", True),
                initial_value=led_config.get("initial_value", False),
            )
            if led_config.get("reset_skip", False):
                self._reset_skip_set.add(f"led:{led_id}")
        return leds

    def _init_rgb_leds(self, rgb_leds_config: Dict[str, Any]) -> Dict[str, RGBLED]:
        from picozero import RGBLED

        rgb_leds = {}
        for rgb_led_id, rgb_led_config in rgb_leds_config.items():
            rgb_leds[rgb_led_id] = RGBLED(
                red=rgb_led_config["port_red"],
                green=rgb_led_config["port_green"],
                blue=rgb_led_config["port_blue"],
                active_high=rgb_led_config.get("active_high", True),
                initial_value=rgb_led_config.get("initial_value", (0, 0, 0)),
                pwm=rgb_led_config.get("pwm", True),
            )
            if rgb_led_config.get("reset_skip", False):
                self._reset_skip_set.add(f"rgb_led:{rgb_led_id}")
        return rgb_leds

    def _init_pots(self, pots_config: Dict[str, Any]) -> Dict[str, Pot]:
        from picozero import Pot

        pots = {}
        for pot_id, pot_config in pots_config.items():
            pots[pot_id] = Pot(
                pin=pot_config["port"],
                active_state=pot_config.get("active_state", True),
                threshold=pot_config.get("threshold", 0.5),
            )
        return pots

    def _init_out_midis(self, out_midis_config: Dict[str, Any]) -> Dict[str, "OutMIDI"]:  # noqa
        from common.midis import OutMIDI

        out_midis = {}
        for out_midi_id, out_midi_config in out_midis_config.items():
            out_midis[out_midi_id] = OutMIDI(
                uart=out_midi_config["uart"],
                port=out_midi_config["port"],
                default_channel=out_midi_config.get("default_channel", None),
                name=f"OMD_{out_midi_id}",
                debug=self._debug,
            )
            if out_midi_config.get("is_default", False):
                if self._out_midi_default is None:
                    self._out_midi_default = out_midis[out_midi_id]
                else:
                    raise ValueError("Only one MIDI Output can be set as default")
        return out_midis

    async def destroy(self) -> None:
        self._reset_skip_set.clear()
        self.reset()
        self._reset_skip_set = None

        for button in self._buttons.values():
            await button.destroy()
        self._buttons = None
        self._button_combinations = None

        for led in self._leds.values():
            led.close()
        self._leds = None

        for rgb_led in self._rgb_leds.values():
            rgb_led.close()
        self._rgb_leds = None

        for pot in self._pots.values():
            pot.close()
        self._pots = None

        for out_midi in self._out_midis.values():
            out_midi.destroy()
        self._out_midis = None
        self._out_midi_default = None

        return None


del micropython
