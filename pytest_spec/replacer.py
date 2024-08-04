"""Module contains method for replace operation.

Additional method are necessary because self is not yet defined and module
doesn't have access to it.

:author: Pawel Chomicki
"""

from pytest_spec.patch import pytest_collection_modifyitems, pytest_runtest_logreport, pytest_runtest_logstart


def logstart_replacer(self, nodeid, location):
    def wrapper():
        return pytest_runtest_logstart(self, nodeid, location)

    return wrapper()


def report_replacer(self, report):
    def wrapper():
        return pytest_runtest_logreport(self, report)

    return wrapper()


def modifyitems_replacer(session, config, items):
    def wrapper():
        return pytest_collection_modifyitems(session, config, items)

    return wrapper()
