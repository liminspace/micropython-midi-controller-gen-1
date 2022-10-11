import micropython
import uasyncio

from common.tools import async_partial

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Any, Dict, Optional

    from common.bank_managers import BankManager
    from common.boards import Board


class FunctionCatalogBase:
    NAME: str
    FUNCTIONS_MAP: Dict[str, str]
    _function_wrapper: Optional[callable] = None
    _loop: uasyncio.Loop

    def __init__(self):
        self._loop = uasyncio.get_event_loop()

    @micropython.native
    def _get_func_by_name(self, name: str) -> callable:
        return getattr(self, self.FUNCTIONS_MAP[name])

    @micropython.native
    async def execute(self, name: str, kwargs: Dict) -> Any:
        func = self._get_func_by_name(name=name)
        return await self._execute_func(func=func, **kwargs)

    @micropython.native
    async def _execute_func(self, func, **kwargs) -> Any:
        is_async = kwargs.pop("async", False)

        if self._function_wrapper:
            task = self._function_wrapper(func=func, **kwargs)
        else:
            task = func(**kwargs)

        if is_async:
            self._loop.create_task(task)
            return None

        return await task

    @micropython.native
    def get_command_func(self, name: str) -> callable:
        func = self._get_func_by_name(name=name)
        return async_partial(self._execute_func, func=func)


class FunctionCatalogBoardBase(FunctionCatalogBase):
    _board: Board

    def __init__(self, board: Board):
        super().__init__()
        self._board = board


class FunctionCatalogBankManagerBase(FunctionCatalogBase):
    _bank_manager: BankManager

    def __init__(self, bank_manager: BankManager):
        super().__init__()
        self._bank_manager = bank_manager


del micropython
