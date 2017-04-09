# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
from mock import Mock


class FakeHook(object):
    def __init__(self, *args, **kwargs):
        self.cat = kwargs.get('cat', ' ')
        self.letter = kwargs.get('letter', ' ')
        self.word = kwargs.get('word', ' ')

    def pytest_report_teststatus(self, report):
        return self.cat, self.letter, self.word


class FakeOption(object):
    def __init__(self, spec):
        self.spec = spec


class FakeConfig(object):
    def __init__(self, spec=True, *args, **kwargs):
        self.hook = FakeHook(*args, **kwargs)
        self.option = FakeOption(spec=spec)

    def getini(self, option):
        if option == 'spec_header_format':
            return '{path}::{class_name}'
        elif option == 'spec_test_format':
            return '[{result}]  {name}'
        else:
            raise TypeError('Option {} is not supported in the test'.format(option))


class FakeStats(object):
    def setdefault(self, first, second):
        return []


class FakeSelf(object):
    def __init__(self, *args, **kwargs):
        self.config = FakeConfig(*args, **kwargs)
        self.currentfspath = None
        self._tw = Mock()
        self.stats = FakeStats()

    @property
    def tw(self):
        return self._tw


class FakeReport(object):
    def __init__(self, nodeid, *args, **kwargs):
        self.fspath = __file__
        self.nodeid = nodeid
        self.passed = kwargs.get('passed', True)
        self.failed = kwargs.get('failed', False)
        self.skipped = kwargs.get('skipped', False)
