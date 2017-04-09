# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import pytest

from asserts import assert_equal
from mock import patch
from pytest_spec.replacer import logstart_replacer, report_replacer


class TestReplacer(object):

    @patch('pytest_spec.replacer.pytest_runtest_logstart')
    def test__logstart_replacer__returns_result_of_pytest_runtest_logstart_method(self, method_mock):
        method_mock.return_value = 'test'
        result = logstart_replacer('self', 'nodeid', 'location')
        assert_equal(result, 'test')

    @patch('pytest_spec.replacer.pytest_runtest_logreport')
    def test__report_replacer__returns_result_of_pytest_runtest_logreport_method(self, method_mock):
        method_mock.return_value = 'test'
        result = report_replacer('self', 'report')
        assert_equal(result, 'test')


if __name__ == '__main__':
    pytest.main()
