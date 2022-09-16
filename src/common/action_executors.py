import sys

import micropython
import uasyncio

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from types import ModuleType
    from typing import Any, Dict, List, Tuple, Union

    from common.boards import Board
    from common.function_catalogs.base import FunctionCatalogBase


class ActionExecutor:
    _catalogs: Dict[str, FunctionCatalogBase]
    _compiled_funcs_cache: Dict[str, callable]
    _ignore_action_errors: bool
    _loop: uasyncio.Loop

    def __init__(
        self,
        board: Board,
        config: ModuleType,
    ):
        self._loop = uasyncio.get_event_loop()
        self._board = board
        self._debug = config.DEBUG
        self._ignore_action_errors = config.IGNORE_ACTION_ERRORS
        self._catalogs = {}
        self._compiled_funcs_cache = {}
        self._add_default_function_catalogs()
        self._add_board_based_function_catalogs()

    def add_catalog(self, catalog: FunctionCatalogBase) -> None:
        if catalog.NAME in self._catalogs:
            raise ValueError(f"function catalog with name `{catalog.NAME}` already exists")
        self._catalogs[catalog.NAME] = catalog
        return None

    def remove_catalog(self, name: str) -> None:
        self._catalogs.pop(name)
        return None

    def _add_default_function_catalogs(self) -> None:
        from common.function_catalogs.fc_time import TIMEFunctionCatalog

        self.add_catalog(catalog=TIMEFunctionCatalog())
        return None

    def _add_board_based_function_catalogs(self) -> None:
        from common.function_catalogs.fc_led import LEDFunctionCatalog
        from common.function_catalogs.fc_midi import MIDIFunctionCatalog
        from common.function_catalogs.fc_rgbled import RGBLEDFunctionCatalog

        if self._board.leds:
            self.add_catalog(catalog=LEDFunctionCatalog(board=self._board))
        if self._board.rgb_leds:
            self.add_catalog(catalog=RGBLEDFunctionCatalog(board=self._board))
        if self._board.out_midis:
            self.add_catalog(catalog=MIDIFunctionCatalog(board=self._board))
        return None

    @micropython.native
    def _resolve_name(self, name: str) -> Tuple[FunctionCatalogBase, str]:
        catalog_name, function_name = name.split(":", 1)
        catalog = self._catalogs[catalog_name]
        return catalog, function_name

    @micropython.native
    async def execute_set(
        self,
        actions: List[Tuple[str, Union[str, callable], Dict[str, Any]]],
        wait: bool = True,
    ) -> None:
        for action in actions:
            task = self._loop.create_task(self.execute(action=action))
            if wait:
                await task
        return None

    @micropython.native
    async def execute(
        self,
        action: Tuple[str, Union[str, callable], Dict[str, Any]],
    ) -> Any:
        desc, func_or_name, kwargs = action
        if isinstance(func_or_name, str):
            catalog, function_name = self._resolve_name(name=func_or_name)
            task = catalog.execute(name=function_name, kwargs=kwargs)
        else:
            task = func_or_name(**kwargs)

        try:
            return await task
        except Exception as e:
            if self._ignore_action_errors:
                if self._debug:
                    sys.print_exception(e)
                return None
            raise e

    def get_action_func(self, name: str) -> callable:
        if name in self._compiled_funcs_cache:
            return self._compiled_funcs_cache[name]
        catalog, function_name = self._resolve_name(name=name)
        func = catalog.get_action_func(name=function_name)
        self._compiled_funcs_cache[name] = func
        return func

    def destroy(self) -> None:
        self._compiled_funcs_cache = None
        self._catalogs = None
        self._loop = None
        return None


class ActionState:
    _state_ix: int
    _action_executor: ActionExecutor
    _action_sets: List[Tuple[str, List[Tuple]]]
    _states_number: int
    _init_state_ix: int

    def __init__(
        self,
        action_executor: ActionExecutor,
        action_sets: List[Tuple[str, List[Tuple]]],
        init_state_ix: int = -1,
    ):
        self._action_executor = action_executor
        self._state_ix = init_state_ix
        self._init_state_ix = init_state_ix
        self._action_sets = action_sets
        self._states_number = len(self._action_sets)

    def reset(self) -> None:
        self._state_ix = self._init_state_ix
        return None

    @micropython.native
    async def __call__(self, ix_inc: int = 1, **kwargs) -> None:
        if not self._states_number:
            return None
        if self._state_ix == -1 and ix_inc < 0:
            ix_inc += 1
        state_ix = self._state_ix + ix_inc
        if not (0 <= state_ix < self._states_number):
            state_ix = state_ix % self._states_number
        action_set = self._action_sets[state_ix]
        await self._action_executor.execute_set(actions=action_set[1])
        self._state_ix = state_ix
        return None

    def destroy(self) -> None:
        self._state_ix = None
        self._init_state_ix = None
        self._action_sets = None
        self._states_number = None
        self._action_executor = None


del micropython
