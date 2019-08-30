#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
import click

from pay.manager import Manager
from pay.events import EventFactory


logging.config.fileConfig("logging.ini")
LOG = logging.getLogger(__name__)
print(LOG)


@click.command()
@click.argument("payloads", type=click.File("rb"), default="-")
def cli(payloads: click.File):

    manager = Manager()

    for payload in payloads:
        message = payload.decode("utf-8").strip()
        event = EventFactory.create(message, manager)
        event.handle()

    LOG.info(manager)


if __name__ == "__main__":
    cli()
