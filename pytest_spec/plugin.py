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
