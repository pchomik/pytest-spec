"""
:author: Pawel Chomicki
"""

import unittest
from unittest.mock import Mock, call, patch

from pytest_spec.plugin import pytest_addoption, pytest_configure


class FakeOption:
    def __init__(self, spec=False):
        self.spec = spec
        self.verbose = 0


class FakeConfig:
    def __init__(self, spec):
        self.option = FakeOption(spec=spec)


class TestPlugin(unittest.TestCase):
    def setUp(self):
        self.mock = Mock()

    def test__pytest_adoption__gets_general_group(self):
        pytest_addoption(self.mock)
        self.mock.assert_has_calls([call.getgroup("general")])

    def test__pytest_adoption__adds_spec_option(self):
        pytest_addoption(self.mock)
        self.mock.assert_has_calls(
            [
                call.getgroup().addoption(
                    "--spec",
                    action="store_true",
                    dest="spec",
                    help="Print test result in specification format",
                )
            ]
        )

    @patch("importlib.reload")
    def test__pytest_configure__should_not_reload_configuration(self, imp_mock):
        pytest_configure(FakeConfig(spec=False))
        self.assertEqual(len(imp_mock.mock_calls), 0)

    @patch("importlib.reload")
    def test__pytest_configure__reloads_pytest_after_patching(self, imp_mock):
        pytest_configure(FakeConfig(spec=True))
        self.assertEqual(len(imp_mock.mock_calls), 1)


if __name__ == "__main__":
    unittest.main()
