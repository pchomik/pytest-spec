# -*- coding: utf-8 -*-
"""Module contains command line option definition and logic needed to enable new formatting.

:author: Pawel Chomicki
"""
from .replacer import logstart_replacer, report_replacer


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        '--spec',
        action='store_true',
        dest='spec',
        help='Print test result in specification format'
    )

    # register config options
    parser.addini(
        'spec_header_format',
        default='{path}::{class_name}',
        help='The format of the test headers when using the spec plugin'
    )
    parser.addini(
        'spec_test_format',
        default='[{result}]  {name}',
        help='The format of the test results when using the spec plugin'
    )


def pytest_configure(config):
    if config.option.spec:
        import imp
        import _pytest
        _pytest.terminal.TerminalReporter.pytest_runtest_logstart = logstart_replacer
        _pytest.terminal.TerminalReporter.pytest_runtest_logreport = report_replacer
        imp.reload(_pytest)
