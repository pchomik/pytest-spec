# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import pytest

from asserts import assert_equal
from mock import Mock, call, patch
from pytest_spec.plugin import pytest_addoption, pytest_configure
from fixtures import FakeConfig


class TestPlugin(object):

    def setup_class(self):
        self.mock_obj = Mock()

    def test__pytest_adoption__gets_general_group(self):
        pytest_addoption(self.mock_obj)
        self.mock_obj.assert_has_calls([call.getgroup('general')])

    def test__pytest_adoption__adds_spec_option(self):
        pytest_addoption(self.mock_obj)
        self.mock_obj.assert_has_calls([call.getgroup().addoption(
            '--spec',
            action='store_true',
            dest='spec',
            help='Print test result in specification format')])

    @patch('imp.reload')
    def test__pytest_configure__should_not_reload_configuration(self, imp_mock):
        pytest_configure(FakeConfig(spec=False))
        assert_equal(len(imp_mock.mock_calls), 0)

    @patch('imp.reload')
    def test__pytest_configure__reloads_pytest_after_patching(self, imp_mock):
        pytest_configure(FakeConfig(spec=True))
        assert_equal(len(imp_mock.mock_calls), 1)


if __name__ == '__main__':
    pytest.main()
