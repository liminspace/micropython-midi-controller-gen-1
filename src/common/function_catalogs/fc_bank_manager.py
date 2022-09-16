import micropython

from common.function_catalogs.base import FunctionCatalogBankManagerBase

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Any

    from common.action_executors import ActionState


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


class GlobalStateFunctionCatalog(FunctionCatalogBankManagerBase):
    NAME = "STATE"
    FUNCTIONS_MAP = {
        "CALL_NEXT": "call_next_global_state",
        "CALL_PREV": "call_prev_global_state",
        "RESET": "set_initial_global_state",
    }

    @micropython.native
    async def _function_wrapper(self, func, **kwargs) -> Any:
        state_id = kwargs.pop("id")
        state = self._bank_manager.global_states[state_id]
        return await func(state=state, **kwargs)

    @micropython.native
    async def call_next_global_state(self, state: ActionState) -> None:
        await state()
        return None

    @micropython.native
    async def call_prev_global_state(self, state: ActionState) -> None:
        await state(ix_inc=-1)
        return None

    @micropython.native
    async def set_initial_global_state(self, state: ActionState) -> None:
        state.reset()
        return None


del micropython
