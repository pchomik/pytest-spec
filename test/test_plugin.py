# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import unittest

from mock import Mock, call
from pytest_spec.plugin import pytest_addoption


class TestPlugin(unittest.TestCase):
    def setUp(self):
        self.parser = Mock()

    def test_pytest_adoption_gets_general_group(self):
        pytest_addoption(self.parser)
        self.parser.assert_has_calls(call.getgroup('general'))

    def test_pytest_adoption_adds_spec_option(self):
        pytest_addoption(self.parser)
        self.parser.assert_has_calls(call.getgroup().addoption('--spec',
                                                               action='store_true',
                                                               dest='spec',
                                                               help='Print test result in specification format'))

    def test_should_be_failed(self):
        self.assertEqual(1, 2)


@unittest.skip("to skip")
class TestPlugin2(unittest.TestCase):
    def test_should_be_skipped(self):
        self.assertEqual(1, 1)


class TestHelper(unittest.TestCase):
    pass


class TestPlugin3(TestHelper):
    def test_should_be_passed_when_is_subclassed(self):
        self.assertEqual(1, 1)
