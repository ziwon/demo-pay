#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pay.events import Event

import pytest


def test_create_event_error1(factory, manager):
    with pytest.raises(ValueError):
        message = "Add"
        factory.create(message, manager)


def test_create_event_error2(factory, manager):
    with pytest.raises(ValueError):
        message = "Add Jane"
        factory.create(message, manager)


def test_create_event_success(factory, manager):
    message = "Add Jane 4111111111111111 $1000"
    event: Event = factory.create(message, manager)
    assert event.kind == "Add"
    assert event.name == "Jane"
    assert event.params == [4111111111111111, 1000]
