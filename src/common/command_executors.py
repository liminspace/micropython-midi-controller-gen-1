import sys

import micropython
import uasyncio

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from types import ModuleType
    from typing import Any, Dict, List, Optional, Tuple

    from common.boards import Board
    from common.function_catalogs.base import FunctionCatalogBase


class CommandExecutor:
    _catalogs: Dict[str, FunctionCatalogBase]
    _compiled_funcs_cache: Dict[str, callable]
    _ignore_command_errors: bool
    _loop: uasyncio.Loop

    def __init__(
        self,
        board: Board,
        config: ModuleType,
    ):
        self._loop = uasyncio.get_event_loop()
        self._board = board
        self._debug = config.DEBUG
        self._ignore_command_errors = config.IGNORE_COMMAND_ERRORS
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
        commands: List[Dict],
        wait: bool = True,
    ) -> None:
        for command in commands:
            task = self._loop.create_task(self.execute(command=command))
            if wait:
                await task
        return None

    @micropython.native
    async def execute(
        self,
        command: Dict,
    ) -> Any:
        func_or_name = command["FUNC"]
        kwargs = command.get("ARGS", {})
        if isinstance(func_or_name, str):
            catalog, function_name = self._resolve_name(name=func_or_name)
            task = catalog.execute(name=function_name, kwargs=kwargs)
        else:
            task = func_or_name(**kwargs)

        try:
            return await task
        except Exception as e:
            if self._ignore_command_errors:
                if self._debug:
                    sys.print_exception(e)
                return None
            raise e

    def get_command_func(self, name: str) -> callable:
        if name in self._compiled_funcs_cache:
            return self._compiled_funcs_cache[name]
        catalog, function_name = self._resolve_name(name=name)
        func = catalog.get_command_func(name=function_name)
        self._compiled_funcs_cache[name] = func
        return func

    def destroy(self) -> None:
        self._compiled_funcs_cache = None
        self._catalogs = None
        self._loop = None
        return None


class CommandStateGroup:
    _state_ix: int
    _command_executor: CommandExecutor
    _name: str
    _vars: Dict
    _states: List[Dict]
    _states_number: int
    _init_state_ix: int
    _state_ix_by_id: Dict

    def __init__(
        self,
        command_executor: CommandExecutor,
        states: List[Dict],
        name: Optional[str] = None,
        state_vars: Optional[Dict] = None,
        init_state_ix: int = -1,
    ):
        self._name = name or ""
        self._vars = (state_vars or {}).copy()
        self._command_executor = command_executor
        self._state_ix = init_state_ix
        self._init_state_ix = init_state_ix
        self._states = states
        self._states_number = len(self._states)
        self._make_state_ix_by_id_index()

    def _make_state_ix_by_id_index(self) -> None:
        self._state_ix_by_id = {}
        for ix, state in enumerate(self._states):
            state_id = state.get("ID", str(ix))
            if state_id in self._state_ix_by_id:
                raise RuntimeError(
                    f"Duplicate state id `{state_id}` in CommandStateGroup with name `{self._name}`"
                )
            self._state_ix_by_id[state_id] = ix

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
        state = self._states[state_ix]
        await self._command_executor.execute_set(commands=state["CMD"])
        self._state_ix = state_ix
        return None

    def destroy(self) -> None:
        self._name = None
        self._vars = None
        self._command_executor = None
        self._state_ix = None
        self._init_state_ix = None
        self._states = None
        self._states_number = None


del micropython
