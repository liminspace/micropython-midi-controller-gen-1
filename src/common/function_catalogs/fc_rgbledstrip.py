import micropython

from common.function_catalogs.base import FunctionCatalogBoardBase

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Any, List, Tuple

    from common.rgb_led_strips import RGBLedStrip


class RGBLEDStripFunctionCatalog(FunctionCatalogBoardBase):
    NAME = "RGB_LED_STRIP"
    FUNCTIONS_MAP = {
        "OFF": "off",
        "ON": "on",
        "COLOR": "color",
        "COLORS": "colors",
        "COLOR_ALL": "color_all",
    }

    @micropython.native
    async def _function_wrapper(self, func, **kwargs) -> Any:
        rgb_led_strip_id = kwargs.pop("id")
        rgb_led_strip = self._board.rgb_led_strips[rgb_led_strip_id]
        return await func(rgb_led_strip=rgb_led_strip, **kwargs)

    @micropython.native
    async def off(self, rgb_led_strip: RGBLedStrip) -> None:
        rgb_led_strip.off()
        return None

    @micropython.native
    async def on(self, rgb_led_strip: RGBLedStrip) -> None:
        rgb_led_strip.on()
        return None

    @micropython.native
    async def color(self, rgb_led_strip: RGBLedStrip, ix: int, val: Tuple[int, ...]) -> None:
        rgb_led_strip.set_color(led_ix=ix, color=val)
        return None

    @micropython.native
    async def colors(self, rgb_led_strip: RGBLedStrip, val: List[Tuple[int, ...]]) -> None:
        rgb_led_strip.set_colors(colors=val)
        return None

    @micropython.native
    async def color_all(self, rgb_led_strip: RGBLedStrip, val: Tuple[int, ...]) -> None:
        rgb_led_strip.set_color_for_all(color=val)
        return None


del micropython
