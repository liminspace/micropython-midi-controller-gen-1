from typing import Callable, Dict, List, Optional, Tuple

import click
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo

from .tools import device_details_to_print

DEVICE_CHECKERS: Dict[str, List[Callable[[ListPortInfo], bool]]] = {
    "Raspberry Pi Pico": [
        lambda d: "VID:PID=2E8A:0005" in d.hwid and d.manufacturer == "MicroPython",
    ],
}


@click.command()
def detect() -> Optional[Tuple[str, ListPortInfo]]:
    detected_devices: List[Tuple[str, ListPortInfo]] = []
    devices: List[ListPortInfo] = comports()
    for device in devices:
        detected_devices.extend(
            (possible_device_name, device)
            for possible_device_name, checkers in DEVICE_CHECKERS.items()
            if any(checker(device) for checker in checkers)
        )
    if not detected_devices:
        click.echo("❌ No devices detected", err=True)
        raise click.Abort()

    if len(detected_devices) > 1:
        devices_details = [
            device_details_to_print(known_name=known_name, device=device)
            for known_name, device in detected_devices
        ]
        nl = "\n"
        click.echo(f"❌ Found more than one device:\n{nl.join(devices_details)}", err=True)
        raise click.Abort()

    known_name, device = detected_devices[0]
    device_details = device_details_to_print(known_name=known_name, device=device)
    click.echo(f"✅ Found device:\n{device_details}")

    return known_name, device
