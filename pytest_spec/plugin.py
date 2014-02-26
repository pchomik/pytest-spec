# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        '--spec',
        action='store_true',
        help='Print test result in specification format'
    )


def pytest_runtest_logreport(report):
    pass


def pytest_report_header(config, startdir):
    pass


def pytest_runtest_setup(item):
    pass


def pytest_runtest_logstart(nodeid, location):
    pass


def pytest_report_teststatus(report):
    pass
