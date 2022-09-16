import micropython

from common.function_catalogs.base import FunctionCatalogBoardBase

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Any, Optional

    from common.midis import OutMIDI


class MIDIFunctionCatalog(FunctionCatalogBoardBase):
    NAME = "MIDI"
    FUNCTIONS_MAP = {
        "CC": "send_control_change",
        "PC": "send_program_change",
    }

    @micropython.native
    async def _function_wrapper(self, func, **kwargs) -> Any:
        out_midi_id = kwargs.pop("id", None)
        if out_midi_id is None:
            out_midi = self._board.out_midi_default
            if out_midi is None:
                raise ValueError("default OUT MIDI is not set")
        else:
            out_midi = self._board.out_midis[out_midi_id]
        return await func(out_midi=out_midi, **kwargs)

    @micropython.native
    async def send_control_change(
        self,
        out_midi: OutMIDI,
        num: int,
        val: int = 0,
        ch: Optional[int] = None,
    ) -> None:
        await out_midi.send_control_change(num=num, val=val, channel=ch)
        return None

    @micropython.native
    async def send_program_change(
        self,
        out_midi: OutMIDI,
        num: int,
        ch: Optional[int] = None,
    ) -> None:
        await out_midi.send_program_change(num=num, channel=ch)
        return None


del micropython
