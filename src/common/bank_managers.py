import micropython

from common.action_executors import ActionState
from common.buttons import ButtonCombination

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from types import ModuleType
    from typing import Dict, List, Tuple

    from common.action_executors import ActionExecutor
    from common.boards import Board


class BankManager:
    _banks: Tuple[Dict]
    _bank_by_name: Dict[str, Dict]
    _banks_number: int

    _board: Board
    _action_executor: ActionExecutor

    _global_states: Dict[str, ActionState]

    _bank_ix: int

    def __init__(
        self,
        board: Board,
        action_executor: ActionExecutor,
        config: ModuleType,
    ):
        self._bank_ix = -1
        self._board = board
        self._action_executor = action_executor
        self._global_states = {}
        self._update_action_executor()
        self._load_banks(path=config.BANKS_PATH)

    @property
    def bank_ix(self) -> int:
        return self._bank_ix

    @property
    def global_states(self) -> Dict[str, ActionState]:
        return self._global_states

    def _update_action_executor(self) -> None:
        from common.function_catalogs.fc_bank_manager import BankFunctionCatalog, GlobalStateFunctionCatalog

        bank_catalog = BankFunctionCatalog(bank_manager=self)
        self._action_executor.add_catalog(catalog=bank_catalog)

        global_state_catalog = GlobalStateFunctionCatalog(bank_manager=self)
        self._action_executor.add_catalog(catalog=global_state_catalog)
        return None

    def _clear_action_executor(self) -> None:
        from common.function_catalogs.fc_bank_manager import BankFunctionCatalog, GlobalStateFunctionCatalog

        self._action_executor.remove_catalog(name=BankFunctionCatalog.NAME)
        self._action_executor.remove_catalog(name=GlobalStateFunctionCatalog.NAME)
        return None

    def _load_banks(self, path: str) -> None:
        from common.tools import load_module_object

        profile = load_module_object(path=path, dot_number=2, expected_type=dict)
        if not profile:
            raise ValueError("profile is empty")
        if not profile.get("banks"):
            raise ValueError("must be loaded at least one bank")
        profile["banks"] = tuple(profile["banks"])
        bank_by_name = {}
        for bank in profile["banks"]:
            self._compile_bank(bank)
            name = bank["ATTR:NAME"]
            if name in bank_by_name:
                raise ValueError(f"duplicated bank name `{name}`")
            bank_by_name[name] = bank
        self._banks = profile["banks"]
        self._bank_by_name = bank_by_name
        self._banks_number = len(self._banks)
        for state_name, state_data in profile.get("global_states", {}).items():
            if not state_data.get("STATES"):
                raise ValueError(f"global state with name {state_name} is empty")
            for actions_set in state_data.get("STATES"):
                self._compile_actions(actions=actions_set[1])
            self._global_states[state_name] = ActionState(
                action_executor=self._action_executor,
                action_sets=state_data.get("STATES"),
            )
        return None

    def _compile_bank(self, bank: Dict) -> None:
        for root_key, root_val in bank.items():
            if root_key.startswith("ON:"):
                self._compile_actions(actions=root_val)
            elif any(map(root_key.startswith, ("BTN:", "COMB:"))):
                for trigger_or_conf_name, val in root_val.items():
                    if trigger_or_conf_name.startswith("ON:"):
                        for action_state in val:
                            self._compile_actions(actions=action_state[1])
        return None

    def _compile_actions(self, actions: List[Tuple]) -> None:
        for i in range(len(actions)):
            action = actions[i]
            if isinstance(action[1], str):
                action = list(action)
                action[1] = self._action_executor.get_action_func(name=action[1])
                actions[i] = tuple(action)
        return None

    @micropython.native
    async def set_bank(self, bank_ix: int) -> None:
        current_bank_ix = self._bank_ix
        current_bank = self._banks[current_bank_ix] if 0 <= current_bank_ix < self._banks_number else None
        if current_bank:
            on_exit_actions = current_bank.get("ON:EXIT", None)
            if on_exit_actions:
                await self._action_executor.execute_set(actions=on_exit_actions)

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

        on_enter_actions = bank.get("ON:ENTER", None)
        if on_enter_actions:
            await self._action_executor.execute_set(actions=on_enter_actions)

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
                        handler=self._get_handler_for_action_sets(
                            action_sets=param_val,
                        ),
                    )
        return None

    @micropython.native
    def _setup_btn_comb(self, buttons_ids: Tuple[str], params: Dict) -> None:
        buttons = tuple(self._board.buttons[button_id] for button_id in buttons_ids)
        on_press = None
        for param_name, param_val in params.items():
            param_type, param_subtype = param_name.split(":", 1)
            if param_type == "ON":
                if param_subtype == "PRESS":
                    on_press = self._get_handler_for_action_sets(
                        action_sets=param_val,
                    )
        if not on_press:
            raise ValueError(f"Button Combinatin for buttons {buttons_ids} does not have any triggers")

        self._board.add_button_combination(
            ButtonCombination(
                buttons=buttons,
                on_press=on_press,
            )
        )
        return None

    @micropython.native
    def _get_handler_for_action_sets(self, action_sets: List[Tuple[str, List[Tuple]]]) -> callable:
        return ActionState(
            action_executor=self._action_executor,
            action_sets=action_sets,
        )

    def destroy(self) -> None:
        self._clear_action_executor()
        self._global_states = None
        self._banks = None
        self._bank_by_name = None
        self._banks_number = None
        self._board = None
        self._action_executor = None
        return None


del micropython
