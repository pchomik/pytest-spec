# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
from .replacer import pytest_runtest_logreport, pytest_runtest_logstart


#------------- MONKEY PATCH OF EXECUTION REPORT ---------------#
import imp
import _pytest
_pytest.terminal.TerminalReporter.pytest_runtest_logstart = pytest_runtest_logstart
_pytest.terminal.TerminalReporter.pytest_runtest_logreport = pytest_runtest_logreport
imp.reload(_pytest)
