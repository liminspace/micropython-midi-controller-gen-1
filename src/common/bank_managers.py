import micropython

from common.buttons import ButtonCombination
from common.command_executors import CommandStateGroup

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from types import ModuleType
    from typing import Dict, List, Optional, Tuple

    from common.boards import Board
    from common.command_executors import CommandExecutor


class BankManager:
    _banks: Tuple[Dict]
    _bank_by_name: Dict[str, Dict]
    _banks_number: int

    _board: Board
    _command_executor: CommandExecutor

    _global_state_groups: Dict[str, CommandStateGroup]

    _bank_ix: int

    def __init__(
        self,
        board: Board,
        command_executor: CommandExecutor,
        config: ModuleType,
    ):
        self._bank_ix = -1
        self._board = board
        self._command_executor = command_executor
        self._global_state_groups = {}
        self._update_command_executor()
        self._load_profile(path=config.PROFILE_PATH)

    @property
    def bank_ix(self) -> int:
        return self._bank_ix

    @property
    def global_state_groups(self) -> Dict[str, CommandStateGroup]:
        return self._global_state_groups

    def _update_command_executor(self) -> None:
        from common.function_catalogs.fc_bank_manager import (
            BankFunctionCatalog,
            GlobalStateGroupFunctionCatalog,
        )

        bank_catalog = BankFunctionCatalog(bank_manager=self)
        self._command_executor.add_catalog(catalog=bank_catalog)

        global_state_group_catalog = GlobalStateGroupFunctionCatalog(bank_manager=self)
        self._command_executor.add_catalog(catalog=global_state_group_catalog)
        return None

    def _clear_command_executor(self) -> None:
        from common.function_catalogs.fc_bank_manager import (
            BankFunctionCatalog,
            GlobalStateGroupFunctionCatalog,
        )

        self._command_executor.remove_catalog(name=BankFunctionCatalog.NAME)
        self._command_executor.remove_catalog(name=GlobalStateGroupFunctionCatalog.NAME)
        return None

    def _load_profile(self, path: str) -> None:
        from common.tools import load_module_object

        profile = load_module_object(path=path, dot_number=2, expected_type=dict)
        if not profile:
            raise ValueError("profile is empty")
        if not profile.get("BANKS"):
            raise ValueError("must be loaded at least one bank")
        profile["BANKS"] = tuple(profile["BANKS"])
        bank_by_name = {}
        for ix, bank in enumerate(profile["BANKS"]):
            self._compile_bank(bank)
            name = bank.get("META:NAME", f"BANK {ix + 1}")
            if name in bank_by_name:
                raise ValueError(f"duplicated bank name `{name}`")
            bank_by_name[name] = bank
        self._banks = profile["BANKS"]
        self._bank_by_name = bank_by_name
        self._banks_number = len(self._banks)
        for state_group_id, state_group in profile.get("GLOBAL_STATE_GROUPS", {}).items():
            if not state_group.get("STATES"):
                raise ValueError(f"global state group with id {state_group_id} is empty")
            for state in state_group["STATES"]:
                self._compile_commands(commands=state["CMD"])
            self._global_state_groups[state_group_id] = CommandStateGroup(
                command_executor=self._command_executor,
                states=state_group["STATES"],
                name=state_group["NAME"],
                state_vars=state_group.get("VARS"),
            )
        return None

    def _compile_bank(self, bank: Dict) -> None:
        for root_key, root_val in bank.items():
            if root_key.startswith("ON:"):
                self._compile_commands(commands=root_val)
            elif any(map(root_key.startswith, ("BTN:", "COMB:"))):
                for trigger_or_conf_name, val in root_val.items():
                    if trigger_or_conf_name.startswith("ON:"):
                        for state in val:
                            self._compile_commands(commands=state["CMD"])
        return None

    def _compile_commands(self, commands: List[Dict]) -> None:
        for command in commands:
            if isinstance(command["FUNC"], str):
                command["FUNC"] = self._command_executor.get_command_func(name=command["FUNC"])
        return None

    @micropython.native
    async def set_bank(self, bank_ix: int) -> None:
        current_bank_ix = self._bank_ix
        current_bank = self._banks[current_bank_ix] if 0 <= current_bank_ix < self._banks_number else None
        if current_bank:
            on_exit_commands = current_bank.get("ON:EXIT", None)
            if on_exit_commands:
                await self._command_executor.execute_set(commands=on_exit_commands)

        new_bank_ix = 0 if bank_ix < 0 else bank_ix % self._banks_number
        bank = self._banks[new_bank_ix]
        self._board.reset()

        for root_key, root_val in bank.items():
            key_type, key_val = root_key.split(":", 1)
            if key_type == "BTN":
                self._setup_btn(button_id=key_val, params=root_val)
            elif key_type == "COMB":
                buttons_ids = key_val.split("+")
                self._setup_btn_comb(buttons_ids=buttons_ids, params=root_val)

        on_enter_commands = bank.get("ON:ENTER", None)
        if on_enter_commands:
            await self._command_executor.execute_set(commands=on_enter_commands)

        self._bank_ix = new_bank_ix

        return None

    @micropython.native
    def _setup_btn(self, button_id: str, params: Dict) -> None:
        button = self._board.buttons[button_id]
        for param_name, param_val in params.items():
            param_type, param_subtype = param_name.split(":", 1)
            if param_type == "ON":
                if param_subtype == "PRESS":
                    button.set_on_press_handler(
                        handler=self._get_handler_for_state_group(
                            states=param_val,
                            name=f"BTN:{button_id}:{param_type}:{param_subtype}",
                        ),
                    )
        return None

    @micropython.native
    def _setup_btn_comb(self, buttons_ids: Tuple[str], params: Dict) -> None:
        buttons = tuple(self._board.buttons[button_id] for button_id in buttons_ids)
        buttons_ids_str = "+".join(buttons_ids)
        on_press = None
        for param_name, param_val in params.items():
            param_type, param_subtype = param_name.split(":", 1)
            if param_type == "ON":
                if param_subtype == "PRESS":
                    on_press = self._get_handler_for_state_group(
                        states=param_val,
                        name=f"COMB:{buttons_ids_str}:{param_type}:{param_subtype}",
                    )
        if not on_press:
            raise ValueError(f"Button Combination `{buttons_ids_str}` does not have any triggers")

        self._board.add_button_combination(
            ButtonCombination(
                buttons=buttons,
                on_press=on_press,
            )
        )
        return None

    @micropython.native
    def _get_handler_for_state_group(
        self,
        states: List[Dict],
        name: Optional[str] = None,
        state_vars: Optional[Dict] = None,
    ) -> callable:
        return CommandStateGroup(
            command_executor=self._command_executor,
            states=states,
            name=name,
            state_vars=state_vars,
        )

    def destroy(self) -> None:
        self._clear_command_executor()
        self._global_states = None
        self._banks = None
        self._bank_by_name = None
        self._banks_number = None
        self._board = None
        self._command_executor = None
        return None


del micropython
