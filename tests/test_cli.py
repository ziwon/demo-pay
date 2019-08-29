#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_cli
.. moduleauthor:: Youngpil Yoon <yngpil.yoon@gmail.com>

This is the test module for the project's command-line interface (CLI)
module.
"""
import logging
from click.testing import CliRunner, Result
import pay.cli as cli
from pay import __version__

# To learn more about testing Click applications, visit the link below.
# http://click.pocoo.org/5/testing/
#


def test_default_argument():
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["input.txt"])
    print(result.output)
