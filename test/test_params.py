# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import pytest

from mock import call
from pytest_spec.patch import pytest_runtest_logreport

from fixtures import *


SPEC_TEST_FORMAT = '[{result}]  {name} {p0}'


@pytest.mark.parametrize("name,version", [
    ("pip", "9.0.1"),
    ("pep8", "1.7.0"),
])
def test_package_is_intalled_at_version(name, version):
    fake_self = FakeSelf()
    pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_Demo_CamelCase'))
    fake_self.tw.write.assert_has_calls([call('    [PASS]  Example Demo CamelCase', green=True)])


if __name__ == '__main__':
    pytest.main()
