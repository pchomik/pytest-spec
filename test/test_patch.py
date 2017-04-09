# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import pytest

from mock import call
from asserts import assert_equal, assert_raises
from pytest_spec.patch import pytest_runtest_logstart, pytest_runtest_logreport

from fixtures import *


class TestPatch(object):

    def test__pytest_runtest_logstart__returns_none(self):
        assert_equal(pytest_runtest_logstart('self', 'nodeid', 'location'), None)

    def test__pytest_runtest_logreport__prints_class_name_before_first_test_result(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::Test_example_demo'))
        fake_self.tw.write.assert_has_calls([call('Test::Second')])

    def test__pytest_runtest_logreport__prints_test_name_and_passed_status(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo'))
        fake_self.tw.write.assert_has_calls([call('    [PASS]  Example demo', green=True)])

    def test__pytest_runtest_logreport__prints_test_name_and_failed_status(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo', passed=False, failed=True))
        fake_self.tw.write.assert_has_calls([call('    [FAIL]  Example demo', red=True)])

    def test__pytest_runtest_logreport__prints_test_name_and_skipped_status(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo', passed=False, skipped=True))
        fake_self.tw.write.assert_has_calls([call('    [SKIP]  Example demo', yellow=True)])

    def test__pytest_runtest_logreport__skips_empty_line_for_first_test(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo'))
        with assert_raises(AssertionError):
            fake_self.tw.write.assert_has_calls([call.line(), call.line()])

    def test__pytest_runtest_logreport__marks_method_marked_by_double_underscores(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test__example__demo'))
        fake_self.tw.write.assert_has_calls([call('    [PASS]  Example demo', green=True)])

    def test__pytest_runtest_logreport__prints_test_name_and_handle_only_single_marker(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test__example'))
        fake_self.tw.write.assert_has_calls([call('    [PASS]  Example', green=True)])

    def test__pytest_runtest_logreport__honors_capitalization_of_words_in_test_name(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_Demo_CamelCase'))
        fake_self.tw.write.assert_has_calls([call('    [PASS]  Example Demo CamelCase', green=True)])


if __name__ == '__main__':
    pytest.main()
