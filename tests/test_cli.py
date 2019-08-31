#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import io
from click.testing import CliRunner, Result
import pay.cli as cli


def test_input_file(runner):
    result: Result = runner.invoke(cli.cli, args=["input.txt"])
    assert result.exit_code == 0


def test_input_stdin(monkeypatch, runner):
    monkeypatch.setattr("sys.stdin", io.StringIO("input.txt"))
    result: Result = runner.invoke(cli.cli, args=None)
    assert result.exit_code == 0
