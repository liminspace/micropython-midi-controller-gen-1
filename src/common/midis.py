import machine
import micropython
import uasyncio
import ustruct
import utime

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Optional

const = micropython.const

MIDI_BAUDRATE = const(31250)
MIDI_CMD_CONTROL_CHANGE = const(176)
MIDI_CMD_PROGRAM_CHANGE = const(192)

# https://fmslogo.sourceforge.io/manual/midi-table.html


class OutMIDI:
    _name: str
    _uart: machine.UART
    _stream_writer: uasyncio.StreamWriter

    _default_channel: Optional[int] = None

    def __init__(
        self,
        uart: int,
        port: int,
        default_channel: Optional[int] = None,
        name: Optional[str] = None,
        debug: bool = False,
    ):
        if name is None:
            name = f"OutMIDI_{id(self)}"
        self._name = name
        self._uart = machine.UART(uart, tx=machine.Pin(port))
        self._init_uart()
        self._stream_writer = uasyncio.StreamWriter(self._uart, {})
        self.set_default_channel(default_channel)
        self._default_channel = default_channel
        self._debug = debug

    def set_default_channel(self, channel: Optional[int]) -> None:
        self._default_channel = channel
        return None

    def _init_uart(self) -> None:
        self._uart.init(baudrate=MIDI_BAUDRATE)
        return None

    def destroy(self) -> None:
        self._stream_writer = None
        self._uart.deinit()
        self._uart = None
        return None

    @micropython.native
    async def send_control_change(
        self,
        num: int,
        val: int = 0,
        channel: Optional[int] = None,
    ) -> None:
        if channel is None:
            if self._default_channel is None:
                raise ValueError("channel must be provided because no default one set")
            channel = self._default_channel
        if self._debug:
            print(f"[{utime.ticks_us()}] SEND MIDI Control Change channel={channel} #{num} value={val}")
        msg = ustruct.pack("bbb", MIDI_CMD_CONTROL_CHANGE + channel - 1, num, val)
        self._stream_writer.write(msg)
        await self._stream_writer.drain()
        return None

    @micropython.native
    async def send_program_change(
        self,
        num: int,
        channel: Optional[int] = None,
    ) -> None:
        if channel is None:
            if self._default_channel is None:
                raise ValueError("channel must be provided because no default one set")
            channel = self._default_channel
        if self._debug:
            print(f"[{utime.ticks_us()}] SEND MIDI Program Change channel={channel} #{num}")
        msg = ustruct.pack("bb", MIDI_CMD_PROGRAM_CHANGE + channel - 1, num)
        self._stream_writer.write(msg)
        await self._stream_writer.drain()
        return None


del micropython, const
