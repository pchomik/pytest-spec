"""
:author: Pawel Chomicki
"""

import unittest
from unittest.mock import Mock, call

import pytest_spec
from pytest_spec.patch import pytest_runtest_logreport, pytest_runtest_logstart


class FakeHook:
    def __init__(self, *args, **kwargs):
        self.cat = kwargs.get("cat", " ")
        self.letter = kwargs.get("letter", " ")
        self.word = kwargs.get("word", " ")

    def pytest_report_teststatus(self, report, config):
        return self.cat, self.letter, self.word


class FakeConfig:
    def __init__(self, *args, **kwargs):
        self.hook = FakeHook(*args, **kwargs)
        self.mapping = {
            "spec_header_format": "{module_path}:",
            "spec_test_format": "{result} {name}",
            "spec_success_indicator": "✓",
            "spec_failure_indicator": "✗",
            "spec_skipped_indicator": "?",
            "spec_indent": "  ",
            "spec_ignore": "FLAKE8",
        }

    def getini(self, option):
        result = self.mapping.get(option, None)
        if not result:
            raise TypeError("Option {} is not supported in the test".format(option))
        return result


class FakeStats:
    def setdefault(self, first, second):
        return []


class FakeSelf:
    def __init__(self, *args, **kwargs):
        self.config = FakeConfig(*args, **kwargs)
        self.currentfspath = None
        self._tw = Mock()
        self.stats = FakeStats()


class FakeReport:
    def __init__(self, nodeid, *args, **kwargs):
        self.nodeid = nodeid
        self.passed = kwargs.get("passed", True)
        self.failed = kwargs.get("failed", False)
        self.skipped = kwargs.get("skipped", False)
        self.docstring_summary = "Test documentation"


class TestPatch(unittest.TestCase):
    def tearDown(self):
        pytest_spec.patch.docstring_summaries = dict()

    def test__pytest_runtest_logstart__returns_none(self):
        self.assertEqual(pytest_runtest_logstart("self", "nodeid", "location"), None)

    def test__pytest_runtest_logreport__returns_none_when_letter_is_missing(self):
        result = pytest_runtest_logreport(FakeSelf(letter=""), FakeReport("Test::Second::Test_example_demo"))
        self.assertIsNone(result)

    def test__pytest_runtest_logreport__returns_none_when_word_is_missing(self):
        result = pytest_runtest_logreport(FakeSelf(word=""), FakeReport("Test::Second::Test_example_demo"))
        self.assertIsNone(result)

    def test__pytest_runtest_logreport__returns_none_when_nodeid_is_wrong_formatted(
        self,
    ):
        result = pytest_runtest_logreport(FakeSelf(), FakeReport(""))
        self.assertIsNone(result)

    def test__pytest_runtest_logreport__prints_class_name_before_first_test_result(
        self,
    ):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport("Test::Second::Test_example_demo"))
        fake_self._tw.write.assert_has_calls([call("Second:")])

    def test__pytest_runtest_logreport__prints_test_name_and_passed_status(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport("Test::Second::test_example_demo"))
        fake_self._tw.write.assert_has_calls([call("Second:"), call("  ✓ Example demo", green=True)])

    def test__pytest_runtest_logreport__prints_test_name_and_failed_status(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(
            fake_self,
            FakeReport("Test::Second::test_example_demo", passed=False, failed=True),
        )
        fake_self._tw.write.assert_has_calls([call("Second:"), call("  ✗ Example demo", red=True)])

    def test__pytest_runtest_logreport__prints_test_name_and_skipped_status(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(
            fake_self,
            FakeReport("Test::Second::test_example_demo", passed=False, skipped=True),
        )
        fake_self._tw.write.assert_has_calls([call("Second:"), call("  ? Example demo", yellow=True)])

    def test__pytest_runtest_logreport__skips_empty_line_for_first_test(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport("Test::Second::test_example_demo"))
        with self.assertRaises(AssertionError):
            fake_self._tw.write.assert_has_calls([call.line(), call.line()])

    def test__pytest_runtest_logreport__marks_method_marked_by_double_underscores(self):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport("Test::Second::test__example__demo"))
        fake_self._tw.write.assert_has_calls([call("Second:"), call("  ✓ Example demo", green=True)])

    def test__pytest_runtest_logreport__prints_test_name_and_handle_only_single_marker(
        self,
    ):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport("Test::Second::test__example"))
        fake_self._tw.write.assert_has_calls([call("Second:"), call("  ✓ Example", green=True)])

    def test__pytest_runtest_logreport__honors_capitalization_of_words_in_test_name(
        self,
    ):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport("Test::Second::test_example_Demo_CamelCase"))
        fake_self._tw.write.assert_has_calls([call("Second:"), call("  ✓ Example Demo CamelCase", green=True)])

    def test__pytest_runtest_longreport__uses_docstring_summary(self):
        fake_self = FakeSelf()
        fake_self.config.mapping["spec_test_format"] = "{result} {docstring_summary}"
        pytest_runtest_logreport(fake_self, FakeReport("Test::Second::test_example_Demo_CamelCase"))
        fake_self._tw.write.assert_has_calls([call("  ✓ Test documentation", green=True)])

    def test__pytest_runtest_longreport__uses_docstring_summary_with_parametrize(self):
        fake_self = FakeSelf()
        fake_self.config.mapping["spec_test_format"] = "{result} {docstring_summary}"
        pytest_runtest_logreport(fake_self, FakeReport("Test::Second::test_example_Demo_CamelCase[10-20-30]"))
        fake_self._tw.write.assert_has_calls([call("  ✓ Test documentation[10-20-30]", green=True)])

    def test__pytest_runtest_longreport__uses_test_name_as_docstring_summary_if_missing(
        self,
    ):
        fake_self = FakeSelf()
        fake_self.config.mapping["spec_test_format"] = "{result} {docstring_summary}"
        fake_report = FakeReport("Test::Second::test_example_Demo_CamelCase")
        fake_report.docstring_summary = None
        pytest_runtest_logreport(fake_self, fake_report)
        fake_self._tw.write.assert_has_calls([call("  ✓ Example Demo CamelCase", green=True)])

    def test__pytest_runtest_logreport__ignores_nodeid_which_matches_ignore_string(
        self,
    ):
        fake_self = FakeSelf()
        pytest_runtest_logreport(fake_self, FakeReport("Test::FLAKE8"))
        assert not fake_self._tw.write.mock_calls

    def test__pytest_runtest_logreport__ignores_nodeid_if_multiple_string_ignore_are_provided(
        self,
    ):
        fake_self = FakeSelf()
        fake_self.config.mapping["spec_ignore"] = "FLAKE8,Something"
        pytest_runtest_logreport(fake_self, FakeReport("Something"))
        assert not fake_self._tw.write.called


if __name__ == "__main__":
    unittest.main()
