import gc
import sys

import uasyncio

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from types import ModuleType
    from typing import List, Optional, Tuple

    from common.action_executors import ActionExecutor
    from common.bank_managers import BankManager
    from common.boards import Board


class App:
    board: Board
    action_executor: ActionExecutor
    bank_manager: BankManager
    loop: uasyncio.Loop
    _actions_on_boot: Optional[List[Tuple]]

    def __init__(self):
        from common.action_executors import ActionExecutor
        from common.bank_managers import BankManager
        from common.boards import Board

        config = self._get_config()
        self.loop = uasyncio.get_event_loop()
        self.board = Board(config=config)
        self.action_executor = ActionExecutor(board=self.board, config=config)
        self.bank_manager = BankManager(
            board=self.board,
            action_executor=self.action_executor,
            config=config,
        )
        self._actions_on_boot = config.ACTIONS_ON_BOOT

    async def run(self) -> None:
        if self._actions_on_boot:
            await self.action_executor.execute_set(actions=self._actions_on_boot)
        self._actions_on_boot = None
        await self.bank_manager.set_bank(0)
        gc.collect()

    async def destroy(self) -> None:
        self.bank_manager.destroy()
        self.board.reset()
        self.action_executor.destroy()
        await self.board.destroy()
        self.board = None
        self.action_executor = None
        self.bank_manager = None
        self.loop = None
        self._actions_on_boot = None

    def _get_config(self) -> ModuleType:
        import config

        try:
            return config
        finally:
            del sys.modules["config"]
