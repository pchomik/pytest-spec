# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import pytest
import unittest

from mock import Mock, call
from pytest_spec.patch import pytest_runtest_logstart, pytest_runtest_logreport


SPEC_TEST_FORMAT = '[{result}]  {name} {p0}'


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
        self.nodeid = nodeid
        self.passed = kwargs.get('passed', True)
        self.failed = kwargs.get('failed', False)
        self.skipped = kwargs.get('skipped', False)


class TestPatch(unittest.TestCase):
    # def test__pytest_runtest_logstart__returns_none(self):
    #     self.assertEqual(pytest_runtest_logstart('self', 'nodeid', 'location'), None)

    # def test__pytest_runtest_logreport__prints_class_name_before_first_test_result(self):
    #     fake_self = FakeSelf()
    #     pytest_runtest_logreport(fake_self, FakeReport('Test::Second::Test_example_demo'))
    #     fake_self.tw.write.assert_has_calls([call('Test::Second')])

    # def test__pytest_runtest_logreport__prints_test_name_and_passed_status(self):
    #     fake_self = FakeSelf()
    #     pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo'))
    #     fake_self.tw.write.assert_has_calls([call('    [PASS]  Example demo', green=True)])

    # def test__pytest_runtest_logreport__prints_test_name_and_failed_status(self):
    #     fake_self = FakeSelf()
    #     pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo', passed=False, failed=True))
    #     fake_self.tw.write.assert_has_calls([call('    [FAIL]  Example demo', red=True)])

    # def test__pytest_runtest_logreport__prints_test_name_and_skipped_status(self):
    #     fake_self = FakeSelf()
    #     pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo', passed=False, skipped=True))
    #     fake_self.tw.write.assert_has_calls([call('    [SKIP]  Example demo', yellow=True)])

    # def test__pytest_runtest_logreport__skips_empty_line_for_first_test(self):
    #     fake_self = FakeSelf()
    #     pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo'))
    #     with self.assertRaises(AssertionError):
    #         fake_self.tw.write.assert_has_calls([call.line(), call.line()])

    # def test__pytest_runtest_logreport__marks_method_marked_by_double_underscores(self):
    #     fake_self = FakeSelf()
    #     pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test__example__demo'))
    #     fake_self.tw.write.assert_has_calls([call('    [PASS]  Example demo', green=True)])

    # def test__pytest_runtest_logreport__prints_test_name_and_handle_only_single_marker(self):
    #     fake_self = FakeSelf()
    #     pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test__example'))
    #     fake_self.tw.write.assert_has_calls([call('    [PASS]  Example', green=True)])

    # def test__pytest_runtest_logreport__honors_capitalization_of_words_in_test_name(self):
    #     fake_self = FakeSelf()
    #     pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_Demo_CamelCase'))
    #     fake_self.tw.write.assert_has_calls([call('    [PASS]  Example Demo CamelCase', green=True)])

    @pytest.mark.parametrize("name,version", [
        ("pip", "9.0.1"),
        ("pep8", "1.7.0"),
    ])
    def test_package_is_intalled_at_version(self, name, version):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_Demo_CamelCase'))
        fake_self.tw.write.assert_has_calls([call('    [PASS]  Example Demo CamelCase', green=True)])


if __name__ == '__main__':
    unittest.main()
