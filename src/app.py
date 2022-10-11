import gc
import sys

import uasyncio

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from types import ModuleType
    from typing import Dict, List, Optional

    from common.bank_managers import BankManager
    from common.boards import Board
    from common.command_executors import CommandExecutor


class App:
    board: Board
    command_executor: CommandExecutor
    bank_manager: BankManager
    loop: uasyncio.Loop
    _commands_on_boot: Optional[List[Dict]]

    def __init__(self):
        from common.bank_managers import BankManager
        from common.boards import Board
        from common.command_executors import CommandExecutor

        config = self._get_config()
        self.loop = uasyncio.get_event_loop()
        self.board = Board(config=config)
        self.command_executor = CommandExecutor(board=self.board, config=config)
        self.bank_manager = BankManager(
            board=self.board,
            command_executor=self.command_executor,
            config=config,
        )
        self._commands_on_boot = config.COMMANDS_ON_BOOT

    async def run(self) -> None:
        if self._commands_on_boot:
            await self.command_executor.execute_set(commands=self._commands_on_boot)
        self._commands_on_boot = None
        await self.bank_manager.set_bank(0)
        gc.collect()

    async def destroy(self) -> None:
        self.bank_manager.destroy()
        self.board.reset()
        self.command_executor.destroy()
        await self.board.destroy()
        self.board = None
        self.command_executor = None
        self.bank_manager = None
        self.loop = None
        self._commands_on_boot = None

    def _get_config(self) -> ModuleType:
        import config

        try:
            return config
        finally:
            del sys.modules["config"]
