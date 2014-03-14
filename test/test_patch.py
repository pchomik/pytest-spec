# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import unittest

from mock import Mock
from pytest_spec.patch import pytest_runtest_logstart, pytest_runtest_logreport


class FakeHook(object):
    def __init__(self, *args, **kwargs):
        self.cat = kwargs.get('cat', ' ')
        self.letter = kwargs.get('letter', ' ')
        self.word = kwargs.get('word', ' ')

    def pytest_report_teststatus(self, report):
        return self.cat, self.letter, self.word


class FakeConfig(object):
    def __init__(self, *args, **kwargs):
        self.hook = FakeHook(*args, **kwargs)


class FakeStats(object):
    def setdefault(self, first, second):
        return []


class FakeSelf(object):
    def __init__(self, *args, **kwargs):
        self.config = FakeConfig(*args, **kwargs)
        self.currentfspath = None
        self._tw = Mock()
        self.stats = FakeStats()


class FakeReport(object):
    def __init__(self, nodeid, *args, **kwargs):
        self.nodeid = nodeid
        self.passed = kwargs.get('passed', True)
        self.failed = kwargs.get('failed', False)
        self.skipped = kwargs.get('skipped', False)


class TestPatch(unittest.TestCase):
    def test__pytest_runtest_logstart__returns_none(self):
        self.assertEqual(pytest_runtest_logstart('self', 'nodeid', 'location'), None)

    def test__pytest_runtest_logreport_first_try(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::Test_example_demo'))
        print fake_self._tw.mock_calls


if __name__ == '__main__':
    unittest.main()
