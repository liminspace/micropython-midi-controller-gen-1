from typing import cast

import click
import yaml

from .cmd_collect import collect
from .cmd_detect import detect
from .cmd_mpy_compile import mpy_compile
from .cmd_reset import reset_hard
from .cmd_upload import upload


@click.group()
@click.option(
    "-c",
    "--config",
    required=True,
    default="boardman.yaml",
    type=str,
    help="Config file",
    show_default=True,
)
@click.pass_context
def cli(ctx, config: str):
    ctx.ensure_object(dict)

    with open(config, "r") as f:
        ctx.obj["config"] = yaml.load(f.read(), yaml.CLoader)


cli.add_command(cast(click.Command, collect))
cli.add_command(cast(click.Command, mpy_compile))
cli.add_command(cast(click.Command, detect))
cli.add_command(cast(click.Command, upload))
cli.add_command(cast(click.Command, reset_hard))
