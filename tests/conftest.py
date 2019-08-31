from click.testing import CliRunner

from pay.events import EventFactory
from pay.manager import Manager

import pytest


@pytest.fixture(scope="function")
def runner(request):
    return CliRunner()


@pytest.fixture(scope="function")
def factory(request):
    return EventFactory()


@pytest.fixture(scope="function")
def manager(request):
    return Manager()
