import uasyncio
import utime


async def debug_run() -> None:
    import gc

    from app import App

    do_print = True
    do_restart = True
    do_memory_monitor = True

    def print_async_exceptin(loop, context):
        if do_print:
            print(utime.ticks_cpu(), "Exception!", loop, context)
        raise context.get("exception", RuntimeError("???"))

    uasyncio.get_event_loop().set_exception_handler(print_async_exceptin)

    if do_print:
        gc.collect()
        print("start")
        print(f"used {gc.mem_alloc()}", f"free {gc.mem_free()}")  # type: ignore

    while True:
        app = App()
        await app.run()

        if do_print:
            await uasyncio.sleep_ms(10)
            gc.collect()
            await uasyncio.sleep_ms(10)
            print("init")
            print(f"used {gc.mem_alloc()}", f"free {gc.mem_free()}")  # type: ignore

        if not do_restart:
            break

        await uasyncio.sleep(10)

        await app.destroy()
        del app

        if do_print:
            await uasyncio.sleep_ms(10)
            gc.collect()
            await uasyncio.sleep_ms(10)
            print("destroy")
            print(f"used {gc.mem_alloc()}", f"free {gc.mem_free()}")  # type: ignore

        await uasyncio.sleep(1)

    if do_memory_monitor:
        while True:
            print(f"used {gc.mem_alloc()}", f"free {gc.mem_free()}")  # type: ignore
            await uasyncio.sleep(1)


async def run() -> None:
    from app import App

    app = App()
    await app.run()


if __name__ == "__main__":
    loop = uasyncio.get_event_loop()
    # loop.create_task(debug_run())
    loop.create_task(run())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
