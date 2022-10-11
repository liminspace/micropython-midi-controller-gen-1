import micropython

from common.function_catalogs.base import FunctionCatalogBankManagerBase

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Any

    from common.command_executors import CommandStateGroup


class BankFunctionCatalog(FunctionCatalogBankManagerBase):
    NAME = "BANK"
    FUNCTIONS_MAP = {
        "SWITCH": "switch_bank_by_index_incrementor",
        "NEXT": "switch_bank_to_next",
        "PREV": "switch_bank_to_prev",
    }

    @micropython.native
    async def switch_bank_by_index_incrementor(self, val: int) -> None:
        await self._bank_manager.set_bank(bank_ix=self._bank_manager.bank_ix + val)
        return None

    @micropython.native
    async def switch_bank_to_next(self) -> None:
        return await self.switch_bank_by_index_incrementor(val=1)

    @micropython.native
    async def switch_bank_to_prev(self) -> None:
        return await self.switch_bank_by_index_incrementor(val=-1)


class GlobalStateGroupFunctionCatalog(FunctionCatalogBankManagerBase):
    NAME = "STATE"
    FUNCTIONS_MAP = {
        "CALL_NEXT": "call_next_global_state",
        "CALL_PREV": "call_prev_global_state",
        "RESET": "set_initial_global_state",
    }

    @micropython.native
    async def _function_wrapper(self, func, **kwargs) -> Any:
        state_group_id = kwargs.pop("id")
        state_group = self._bank_manager.global_state_groups[state_group_id]
        return await func(state_group=state_group, **kwargs)

    @micropython.native
    async def call_next_global_state(self, state_group: CommandStateGroup) -> None:
        await state_group()
        return None

    @micropython.native
    async def call_prev_global_state(self, state_group: CommandStateGroup) -> None:
        await state_group(ix_inc=-1)
        return None

    @micropython.native
    async def set_initial_global_state(self, state_group: CommandStateGroup) -> None:
        state_group.reset()
        return None


del micropython
