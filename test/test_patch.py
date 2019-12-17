# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import unittest

from mock import Mock, call
from pytest_spec.patch import pytest_runtest_logstart, pytest_runtest_logreport


class FakeHook(object):
    def __init__(self, *args, **kwargs):
        self.cat = kwargs.get('cat', ' ')
        self.letter = kwargs.get('letter', ' ')
        self.word = kwargs.get('word', ' ')

    def pytest_report_teststatus(self, report, config):
        return self.cat, self.letter, self.word


class FakeConfig(object):
    def __init__(self, *args, **kwargs):
        self.hook = FakeHook(*args, **kwargs)

    def getini(self, option):
        mapping = {
            'spec_header_format': '{module_path}:',
            'spec_test_format': '{result} {name}',
            'spec_success_indicator': '✓',
            'spec_failure_indicator': '✗',
            'spec_skipped_indicator': '?',
            'spec_indent': '  ',
        }
        result = mapping.get(option, None)
        if not result:
            raise TypeError('Option {} is not supported in the test'.format(
                option)
            )
        return result


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

    def test__pytest_runtest_logreport__returns_none_when_letter_is_missing(self):
        result = pytest_runtest_logreport(FakeSelf(letter=''), FakeReport('Test::Second::Test_example_demo'))
        self.assertIsNone(result)

    def test__pytest_runtest_logreport__returns_none_when_word_is_missing(self):
        result = pytest_runtest_logreport(FakeSelf(word=''), FakeReport('Test::Second::Test_example_demo'))
        self.assertIsNone(result)

    def test__pytest_runtest_logreport__returns_none_when_nodeid_is_wrong_formatted(self):
        result = pytest_runtest_logreport(FakeSelf(), FakeReport(''))
        self.assertIsNone(result)

    def test__pytest_runtest_logreport__prints_class_name_before_first_test_result(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::Test_example_demo'))
        fake_self._tw.write.assert_has_calls([call('Second:')])

    def test__pytest_runtest_logreport__prints_test_name_and_passed_status(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo'))
        fake_self._tw.write.assert_has_calls([
            call('Second:'),
            call('  ✓ Example demo', green=True)
        ])

    def test__pytest_runtest_logreport__prints_test_name_and_failed_status(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo', passed=False, failed=True))
        fake_self._tw.write.assert_has_calls([
            call('Second:'),
            call('  ✗ Example demo', red=True)
        ])

    def test__pytest_runtest_logreport__prints_test_name_and_skipped_status(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo', passed=False, skipped=True))
        fake_self._tw.write.assert_has_calls([
            call('Second:'),
            call('  ? Example demo', yellow=True)
        ])

    def test__pytest_runtest_logreport__skips_empty_line_for_first_test(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_demo'))
        with self.assertRaises(AssertionError):
            fake_self._tw.write.assert_has_calls([call.line(), call.line()])

    def test__pytest_runtest_logreport__marks_method_marked_by_double_underscores(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test__example__demo'))
        fake_self._tw.write.assert_has_calls([
            call('Second:'),
            call('  ✓ Example demo', green=True)
        ])

    def test__pytest_runtest_logreport__prints_test_name_and_handle_only_single_marker(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test__example'))
        fake_self._tw.write.assert_has_calls([
            call('Second:'),
            call('  ✓ Example', green=True)
        ])

    def test__pytest_runtest_logreport__honors_capitalization_of_words_in_test_name(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport('Test::Second::test_example_Demo_CamelCase'))
        fake_self._tw.write.assert_has_calls([
            call('Second:'),
            call('  ✓ Example Demo CamelCase', green=True)
        ])


if __name__ == '__main__':
    unittest.main()
