import gc

import machine
import micropython
import uasyncio
import utime

# noinspection PyUnreachableCode
if False:  # sourcery skip: remove-redundant-if
    from typing import Dict, Iterable, Optional, Tuple


const = micropython.const


class DebugMixin:
    debug: bool = False
    _debug_msg_prefix: str = ""

    def debug_print(self, msg: str, add_time: bool = True) -> None:
        if self.debug:
            msg = f"{self._debug_msg_prefix}{msg}"
            if add_time:
                msg = f"[{utime.ticks_ms()}] {msg}"
            print(msg)
        return None

    def set_debug_msg_prefix(self, s: str) -> None:
        self._debug_msg_prefix = s
        return None


# all values are in ms
BUTTON_DEFAULT_LOOP_SLEEP = const(4)  # sleep in regular loop
BUTTON_DEFAULT_LOOP_SLEEP_ON_PRESS = const(
    4
)  # sleep when button was pressed (first press is detected in the loop)
BUTTON_DEFAULT_LOOP_SLEEP_AFTER_TRIGGER = const(30)  # extra sleep when a handler was triggered
BUTTON_DEFAULT_PRESS_THRESHOLD = const(30)  # how much button must be pressed to trigger a handler


class Button(DebugMixin):
    STATE_DISABLED = 0x00
    STATE_ENABLED = 0x01
    STATE_WAITING_FOR_DISABLE = 0x02

    _id: str
    _name: str
    _pin: machine.Pin
    _loop: uasyncio.Loop
    _on_press: Optional[callable]
    _on_press_pre_handlers: Dict[str, callable]
    _process_task: Optional[uasyncio.Task]

    _state: int = STATE_DISABLED
    _press_at: int = 0
    _loop_sleep: int = BUTTON_DEFAULT_LOOP_SLEEP
    _loop_sleep_on_press: int = BUTTON_DEFAULT_LOOP_SLEEP_ON_PRESS
    _loop_sleep_after_trigger: int = BUTTON_DEFAULT_LOOP_SLEEP_AFTER_TRIGGER
    _press_threshold: int = BUTTON_DEFAULT_PRESS_THRESHOLD

    def __init__(
        self,
        port: int,
        button_id: str,
        enable: bool = True,
        on_press: Optional[callable] = None,
        name: Optional[str] = None,
        debug: bool = False,
    ):
        self._id = button_id
        if name is None:
            name = f"Button_{id(self)}"
        self.debug = debug
        self.set_debug_msg_prefix(f"{name}: ")
        self._name = name
        self._pin = machine.Pin(port, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self._loop = uasyncio.get_event_loop()
        self._on_press_pre_handlers = {}
        self._on_press = None
        if on_press:
            self.set_on_press_handler(on_press)
        self._process_task = None
        if enable:
            self._loop.create_task(self.enable())

    @property
    def id(self) -> str:
        return self._id

    def set_on_press_handler(self, handler: Optional[callable]) -> None:
        self.debug_print(f"set_on_press_handler handler={id(handler)}")
        self._on_press = handler
        return None

    def add_on_press_pre_handler(self, name: str, handler: callable) -> None:
        self.debug_print(f"add_on_press_pre_handler {name=} handler={id(handler)}")
        if name in self._on_press_pre_handlers:
            raise ValueError(f"on press pre handler with name `{name}` already exists")
        self._on_press_pre_handlers[name] = handler
        return None

    def remove_on_press_pre_handler(self, name: str) -> None:
        self.debug_print(f"remove_on_press_pre_handler {name=}")
        self._on_press_pre_handlers.pop(name, None)
        return None

    def clear_on_press_pre_handlers(self) -> None:
        self.debug_print("clear_on_press_pre_handlers")
        self._on_press_pre_handlers.clear()
        return None

    def reset_handlers(self) -> None:
        self.set_on_press_handler(None)
        return None

    async def enable(self) -> None:
        if self._state != self.STATE_DISABLED:
            raise RuntimeError("Button is not DISABLED")
        self.debug_print("enable")
        self._process_task = self._loop.create_task(self._process())
        return None

    async def disable(self, wait: bool = True) -> None:
        if self._state != self.STATE_ENABLED:
            raise RuntimeError("Button is not ENABLED")
        self.debug_print("disable")
        self._state = self.STATE_WAITING_FOR_DISABLE
        self._process_task = None
        if wait:
            while self._state == self.STATE_WAITING_FOR_DISABLE:
                await uasyncio.sleep_ms(1)
            self.debug_print("disable: done")
        else:
            self.debug_print("disable: backgrond")
        return None

    def is_enabled(self) -> bool:
        return self._state == self.STATE_ENABLED

    def is_disabled(self) -> bool:
        return self._state == self.STATE_DISABLED

    def is_waiting_for_disable(self) -> bool:
        return self._state == self.STATE_WAITING_FOR_DISABLE

    @micropython.native
    async def _trigger(
        self,
        handler: callable,
        pre_handlers: Tuple[callable] = (),
    ) -> None:
        if self.debug:
            self.debug_print(
                f"_trigger handler={id(handler)} pre_handlers={[id(ph) for ph in pre_handlers]}"
            )
        if pre_handlers:
            results = await uasyncio.gather(*(pre_handler(button=self) for pre_handler in pre_handlers))
            if not all(results):
                if self.debug:
                    self.debug_print(
                        f"_trigger handler={id(handler)} pre_handlers={[id(ph) for ph in pre_handlers]}: skip"
                    )
                return None
        if self.debug:
            self.debug_print(
                f"_trigger handler={id(handler)} pre_handlers={[id(ph) for ph in pre_handlers]}: call"
            )
        await handler()
        gc.collect()
        return None

    @micropython.native
    async def _process(self) -> None:
        self.debug_print("_process")
        self._state = self.STATE_ENABLED
        last_val = None
        while True:
            if self._state == self.STATE_WAITING_FOR_DISABLE:
                self.debug_print("_process: stop")
                self._state = self.STATE_DISABLED
                break
            was_triggered = was_pressed = False
            val = self._pin.value()
            now = utime.ticks_ms()
            if last_val != val:
                last_val = val
                if val == 1:
                    self._press_at = now
                    was_pressed = True
                else:
                    self._press_at = 0
            if (
                val == 1
                and self._press_at
                and utime.ticks_diff(now, self._press_at) >= self._press_threshold
            ):
                if self._on_press:
                    self.debug_print("_process: on press")
                    self._loop.create_task(
                        self._trigger(
                            handler=self._on_press,
                            pre_handlers=tuple(self._on_press_pre_handlers.values()),
                        ),
                    )
                    await uasyncio.sleep_ms(self._loop_sleep_after_trigger)
                    was_triggered = True
                self._press_at = 0
            if was_pressed and not was_triggered:
                sleep_ms = self._loop_sleep_on_press
            else:
                sleep_ms = self._loop_sleep
            await uasyncio.sleep_ms(sleep_ms)
        return None

    async def destroy(self) -> None:
        """use that method before the instance is going to be deleted"""
        self.debug_print("destroy")
        if self.is_enabled():
            await self.disable(wait=True)
        self.set_on_press_handler(None)
        self.clear_on_press_pre_handlers()
        self._press_at = 0
        self._loop = None
        self._pin = None
        return None

    def __str__(self) -> str:
        return self._name


# all values are in ms
BUTTON_COMBINATION_DEFAULT_SLEEP_AFTER_TRIGGER = const(30)


class ButtonCombination(DebugMixin):
    _id: str
    _name: str
    _loop: uasyncio.Loop
    _buttons: Tuple[Button]
    _on_press: Optional[callable]

    _sleep_after_trigger: int = BUTTON_COMBINATION_DEFAULT_SLEEP_AFTER_TRIGGER

    def __init__(
        self,
        buttons: Iterable[Button],
        on_press: Optional[callable] = None,
        name: Optional[str] = None,
        debug: bool = False,
    ):
        self._buttons = tuple(buttons)
        self._id = "+".join(button.id for button in buttons)
        if name is None:
            name = f"ButtonCombination_{id(self)}"
        self.debug = debug
        self.set_debug_msg_prefix(f"{name}: ")
        self._name = name
        self._loop = uasyncio.get_event_loop()
        self._on_press = None
        if on_press:
            self.set_on_press_handler(on_press)

    @property
    def id(self) -> str:
        return self._id

    @micropython.native
    def set_on_press_handler(self, handler: Optional[callable]) -> None:
        self.debug_print(f"set_on_press_handler handler={id(handler)}")
        if handler:
            if not self._on_press:
                for button in self._buttons:
                    button.add_on_press_pre_handler(
                        name=self._name,
                        handler=self._on_press_pre_handler,
                    )
        else:
            if self._on_press:
                for button in self._buttons:
                    button.remove_on_press_pre_handler(self._name)
        self._on_press = handler
        return None

    @micropython.native
    async def _trigger(self, handler: callable) -> None:
        self.debug_print(f"_trigger handler={id(handler)}: call")
        await handler()
        gc.collect()
        return None

    @micropython.native
    async def _on_press_pre_handler(self, button: Button) -> bool:
        self.debug_print(f"_on_press_pre_handler {button=}")
        if not button._press_at:
            return False
        for other_button in self._buttons:
            if other_button is not button and not other_button._press_at:
                return True
        for btn in self._buttons:
            btn._press_at = 0
        if self._on_press:
            self.debug_print("on press")
            self._loop.create_task(self._trigger(handler=self._on_press))
            await uasyncio.sleep_ms(self._sleep_after_trigger)
        return False

    def destroy(self) -> None:
        """use that method before the instance is going to be deleted"""
        self.debug_print("destroy")
        self.set_on_press_handler(None)
        self._loop = None
        self._buttons = None
        return None

    def __str__(self) -> str:
        return self._name


del micropython, const
