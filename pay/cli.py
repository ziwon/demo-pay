#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

"""
import asyncio
import sys
import logging
import click

from .events import EventFactory

from pay.version import __version__

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info:
    """
    This is an information object that can be used to pass data between CLI functions.
    """

    def __init__(self):  # Note that this object must have an empty constructor.
        self.verbose: int = 4


#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)

# Change the options to below to suit the actual options for your task (or
# tasks).


@click.command()
@click.argument("payloads", type=click.File("rb"), default="-")
@pass_info
def cli(info: Info, payloads: click.File):
    """
    Run pay..
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(payloads))
    loop.close()


async def run(payloads):
    from .manager import Manager

    queue = asyncio.Queue()
    manager = Manager()
    consumer = asyncio.ensure_future(consume(queue, manager))
    await produce(queue, payloads)
    await queue.join()
    consumer.cancel()
    print(manager)


async def produce(queue, payloads):
    for payload in payloads:
        message = payload.decode("utf-8").strip()
        await queue.put(message)


async def consume(queue, manager):
    while True:
        message = await queue.get()
        event = EventFactory.create(message, manager)
        event.handle()
        queue.task_done()
