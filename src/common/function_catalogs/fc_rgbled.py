import micropython

from common.function_catalogs.base import FunctionCatalogBoardBase

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Any, Optional, Tuple, Union

    from picozero import RGBLED


class RGBLEDFunctionCatalog(FunctionCatalogBoardBase):
    NAME = "RGB_LED"
    FUNCTIONS_MAP = {
        "OFF": "off",
        "ON": "on",
        "COLOR": "color",
        "BLINK": "blink",
    }

    @micropython.native
    async def _function_wrapper(self, func, **kwargs) -> Any:
        rgb_led_id = kwargs.pop("id")
        rgb_led = self._board.rgb_leds[rgb_led_id]
        return await func(rgb_led=rgb_led, **kwargs)

    @micropython.native
    async def off(self, rgb_led: RGBLED) -> None:
        rgb_led.off()
        return None

    @micropython.native
    async def on(self, rgb_led: RGBLED) -> None:
        rgb_led.on()
        return None

    @micropython.native
    async def color(self, rgb_led: RGBLED, val: Tuple[int, ...]) -> None:
        rgb_led.color = val
        return None

    @micropython.native
    async def blink(
        self,
        rgb_led: RGBLED,
        on_times: Union[int, Tuple[int, ...]] = 1,
        fade_times: Union[int, Tuple[int, ...]] = 0,
        colors: Tuple[Tuple[int, int, int]] = ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        n: Optional[int] = None,
        wait: bool = False,
        fps: int = 25,
    ) -> None:
        rgb_led.blink(
            on_times=on_times,
            fade_times=fade_times,
            colors=colors,
            n=n,
            wait=wait,
            fps=fps,
        )
        return None


del micropython
