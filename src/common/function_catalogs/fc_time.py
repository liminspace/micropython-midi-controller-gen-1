import micropython
import uasyncio

from common.function_catalogs.base import FunctionCatalogBase


class TIMEFunctionCatalog(FunctionCatalogBase):
    NAME = "TIME"
    FUNCTIONS_MAP = {
        "SLEEP": "sleep_ms",
    }

    @micropython.native
    async def sleep_ms(self, val: int) -> None:
        await uasyncio.sleep_ms(val)
        return None


del micropython
