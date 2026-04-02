"""
:author: Pawel Chomicki
"""

import pytest
import unittest
from unittest.mock import Mock, call, ANY

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
            "spec_container_format": "{sentence}",
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
        self.docstring_summary = ["Test documentation"]
        self.describe_hierarchy = kwargs.get("describe_hierarchy", [])

def fake_container_hierarchy(depth, withDocsring=False):
    if 0 >= depth or depth > 2:
        raise ValueError("Depth should be either 1 or 2")
    
    def describe_my_function(): pass
    def describe_my_other_function(): pass
    
    def describe_my_function_with_docstring():
        """
        my function docstring
        This is text that should be ignored.
        """
        pass

    def describe_my_other_function_with_docstring():
        """
        my other function docstring
        This is text that should be ignored.
        """
        pass

    f1 = describe_my_function_with_docstring if withDocsring else describe_my_function
    f2 = describe_my_other_function_with_docstring if withDocsring else describe_my_other_function
    containers = f1.__name__ + "::" + f2.__name__ if depth == 2 else f1.__name__
    nodeid = f"Test::{containers}::test_example_demo"
    describe_heirarchy = [f1] if depth == 1 else [f2, f1]
    return nodeid, describe_heirarchy

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

    def test__pytest_runtest_logreport__honors_different_type_of_baundaries_between_words(self):
        cases = [
            ("Demo_CamelCase", "Demo Camel Case"),
            ("PDFFile", "PDF File"),
            ("camelCase", "Camel Case"),
            ("PascalCase", "Pascal Case"),
            ("lowerACRONYM", "Lower ACRONYM"),
            ("Word123", "Word 123"),
            ("123Word", "123 Word"),
            ("Office365API", "Office 365 API"),
            ("ACRONYM", "ACRONYM"),
            ("ACRONYMletter", "ACRONY Mletter"),
        ]
        for test_suffix, expected_result in cases:
            with self.subTest(test_suffix=test_suffix, expected_result=expected_result):
                fake_self = FakeSelf()
                pytest_runtest_logreport(fake_self, FakeReport(f"Test::Second::test_{test_suffix}"))
                fake_self._tw.write.assert_has_calls([call("Second:"), call(f"  ✓ {expected_result}", green=True)])

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
        fake_self._tw.write.assert_has_calls([call("  ✓ Example Demo Camel Case", green=True)])

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

@pytest.mark.parametrize("hirearchey_detection_method", ["nodeid", "functions"])
class TestContainerHeirarchey:
    def test__pytest_runtest_logreport__prints_container_name_before_first_test_result(
        self,
        hirearchey_detection_method,
    ):
        fake_self = FakeSelf()
        fake_self.config.mapping["spec_test_format"] = "{name}"
        nodeid, describe_hierarchy = fake_container_hierarchy(depth=1, withDocsring=False)
        if hirearchey_detection_method == "nodeid": describe_hierarchy = None
        
        pytest_runtest_logreport(fake_self, FakeReport(nodeid=nodeid, describe_hierarchy=describe_hierarchy))

        fake_self._tw.write.assert_has_calls([
            call("My function:"),
            call('  Example demo', green=ANY),
        ])

    def test__pytest_runtest_logreport__uses_unit_name_format_for_container_name(
        self,
        hirearchey_detection_method,
    ):
        fake_self = FakeSelf()
        fake_self.config.mapping["spec_container_format"] = "{unit_name}"
        nodeid, describe_hierarchy = fake_container_hierarchy(depth=1, withDocsring=False)
        if hirearchey_detection_method == "nodeid": describe_hierarchy = None

        pytest_runtest_logreport(fake_self, FakeReport(nodeid=nodeid, describe_hierarchy=describe_hierarchy))

        fake_self._tw.write.assert_has_calls([call("my_function:")])

    def test__pytest_runtest_logreport__uses_docstring_summary_format_for_container_name(
        self,
        hirearchey_detection_method,
    ):
        if hirearchey_detection_method == "nodeid":
            pytest.skip("Docstring summary format is not supported when hierarchy is detected by nodeid")

        fake_self = FakeSelf()
        fake_self.config.mapping["spec_container_format"] = "{docstring_summary}"
        nodeid, describe_hierarchy = fake_container_hierarchy(depth=1, withDocsring=True)

        pytest_runtest_logreport(fake_self, FakeReport(nodeid=nodeid, describe_hierarchy=describe_hierarchy))

        fake_self._tw.write.assert_has_calls([call("my function docstring:")])


    def test__pytest_runtest_logreport__uses_sentence_format_when_docstring_summary_format_not_available(
        self, hirearchey_detection_method,
    ):
        fake_self = FakeSelf()
        fake_self.config.mapping["spec_container_format"] = "{docstring_summary}"
        nodeid, describe_hierarchy = fake_container_hierarchy(depth=1, withDocsring=False)
        if hirearchey_detection_method == "nodeid": describe_hierarchy = None

        pytest_runtest_logreport(fake_self, FakeReport(nodeid=nodeid, describe_hierarchy=describe_hierarchy))

        fake_self._tw.write.assert_has_calls([call("My function:")])

    def test__pytest_runtest_logreport__adds_indentation_for_each_nested_container(
        self,
        hirearchey_detection_method,
    ):
        fake_self = FakeSelf()
        indent = fake_self.config.mapping["spec_indent"]
        nodeid, describe_hierarchy = fake_container_hierarchy(depth=2, withDocsring=False)
        if hirearchey_detection_method == "nodeid": describe_hierarchy = None

        pytest_runtest_logreport(fake_self, FakeReport(nodeid=nodeid, describe_hierarchy=describe_hierarchy))

        fake_self._tw.write.assert_has_calls([
            call("My function:"),
            call(indent + 'My other function:'),
        ])

    def test__pytest_runtest_logreport__does_not_print_the_same_container_more_than_once(
        self,
        hirearchey_detection_method,
    ):
        fake_self = FakeSelf()
        fake_self.config.mapping["spec_test_format"] = "{name}"
        nodeid, describe_hierarchy = fake_container_hierarchy(depth=2, withDocsring=False)
        if hirearchey_detection_method == "nodeid": describe_hierarchy = None

        pytest_runtest_logreport(fake_self, FakeReport(nodeid=nodeid, describe_hierarchy=describe_hierarchy))
        pytest_runtest_logreport(fake_self, FakeReport(nodeid=nodeid, describe_hierarchy=describe_hierarchy))

        fake_self._tw.write.assert_has_calls([
            call("Test:"),
            call("My function:"),
            call('  My other function:'),
            call('    Example demo', green=ANY),
            call('    Example demo', green=ANY),
        ])

    def test__pytest_runtest_logreport__does_not_collapse_different_containers_with_the_same_name(
        self,
        hirearchey_detection_method,
    ):
        def create_heirarchy(top):
            def describe_A(): pass
            def describe_B(): pass
            def describe_C(): pass
            return [describe_C, describe_B, describe_A, top]
        
        def describe_I(): pass
        def describe_II(): pass

        fake_self = FakeSelf()
        nodeid1 = f"Test::{describe_I.__name__}::describe_A::describe_B::describe_C::test_example_demo"
        nodeid2 = f"Test::{describe_II.__name__}::describe_A::describe_B::describe_C::test_example_demo"
        hierarchy1 = create_heirarchy(describe_I) if hirearchey_detection_method == "functions" else None
        hierarchy2 = create_heirarchy(describe_II) if hirearchey_detection_method == "functions" else None

        pytest_runtest_logreport(fake_self, FakeReport(nodeid=nodeid1, describe_hierarchy=hierarchy1))
        pytest_runtest_logreport(fake_self, FakeReport(nodeid=nodeid2, describe_hierarchy=hierarchy2))

        fake_self._tw.write.assert_has_calls([
            call("I:"),
            call('  A:'),
            call('    B:'),
            call('      C:'),
        ])

        fake_self._tw.write.assert_has_calls([
            call("II:"),
            call('  A:'),
            call('    B:'),
            call('      C:'),
        ])

if __name__ == "__main__":
    unittest.main()
