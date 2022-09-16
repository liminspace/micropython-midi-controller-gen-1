import micropython

from common.function_catalogs.base import FunctionCatalogBoardBase

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Any, Optional, Union

    from picozero import PWMLED, DigitalLED


class LEDFunctionCatalog(FunctionCatalogBoardBase):
    NAME = "LED"
    FUNCTIONS_MAP = {
        "OFF": "off",
        "ON": "on",
        "BRIGHTNESS": "brightness",
        "BLINK": "blink",
    }

    @micropython.native
    async def _function_wrapper(self, func, **kwargs) -> Any:
        led_id = kwargs.pop("id")
        led = self._board.leds[led_id]
        return await func(led=led, **kwargs)

    @micropython.native
    async def off(self, led: Union[PWMLED, DigitalLED]) -> None:
        led.off()
        return None

    @micropython.native
    async def on(self, led: Union[PWMLED, DigitalLED]) -> None:
        led.on()
        return None

    @micropython.native
    async def brightness(self, led: Union[PWMLED, DigitalLED], val: float) -> None:
        led.brightness = val
        return None

    @micropython.native
    async def blink(
        self,
        led: Union[PWMLED, DigitalLED],
        on_time: int = 1,
        off_time: Optional[int] = None,
        n: Optional[int] = None,
        wait: bool = False,
        fade_in_time: int = 0,
        fade_out_time: Optional[int] = None,
        fps: int = 25,
    ) -> None:
        led.blink(
            on_time=on_time,
            off_time=off_time,
            n=n,
            wait=wait,
            fade_in_time=fade_in_time,
            fade_out_time=fade_out_time,
            fps=fps,
        )
        return None


del micropython
