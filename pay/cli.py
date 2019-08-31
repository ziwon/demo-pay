import click

from pay.logging import LOG
from pay.manager import Manager
from pay.events import EventFactory


@click.command()
@click.argument("payloads", type=click.File("rb"), default="-")
def cli(payloads: click.File):

    LOG.debug(f"input: {payloads}")
    manager = Manager()

    for payload in payloads:
        message = payload.decode("utf-8").strip()
        event = EventFactory.create(message, manager)
        event.handle()

    LOG.debug(f"output: {manager.status()}")
