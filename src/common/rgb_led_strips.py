import machine
import micropython
from neopixel import NeoPixel

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import List, Optional, Tuple


class RGBLedStrip:
    _name: str
    _np: NeoPixel
    _length: int
    _color_map: Optional[Tuple[int, ...]]
    _debug: bool

    def __init__(
        self,
        port: int,
        length: int = 1,
        color_map: Optional[str] = None,
        name: Optional[str] = None,
        debug: bool = False,
    ):
        if name is None:
            name = f"RGBLedStrip_{id(self)}"
        self._name = name
        self._np = NeoPixel(machine.Pin(port), length)
        self._length = length
        if not color_map or color_map == "RGB":
            self._color_map = None
        else:
            self._color_map = tuple(color_map.index(t) for t in "RGB")
        self._debug = debug

    @micropython.native
    def _normalize_color(self, color: Tuple[int, ...]) -> Tuple[int, ...]:
        if self._color_map:
            color = tuple(color[t] for t in self._color_map)
        return color

    @micropython.native
    def set_color(self, led_ix: int, color: Tuple[int, ...]) -> None:
        self._np[led_ix] = self._normalize_color(color)
        self._np.write()
        return None

    @micropython.native
    def set_color_for_all(self, color: Tuple[int, ...]) -> None:
        norm_color = self._normalize_color(color)
        for i in range(self._length):
            self._np[i] = norm_color
        self._np.write()
        return None

    @micropython.native
    def set_colors(self, colors: List[Optional[Tuple[int, ...]]]) -> None:
        for i, color in enumerate(colors):
            if color is None:
                continue
            self._np[i] = self._normalize_color(color)
        self._np.write()
        return None

    @micropython.native
    def off(self) -> None:
        self.set_color_for_all((0, 0, 0))
        return None

    @micropython.native
    def on(self) -> None:
        self.set_color_for_all((255, 255, 255))
        return None


del micropython
