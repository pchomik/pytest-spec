# -*- coding: utf-8 -*-
"""Module contains method that will be replaced by the plugin.

:author: Pawel Chomicki
"""


def pytest_runtest_logstart(self, nodeid, location):
    """Signal the start of running a single test item.

    Hook has to be disabled because additional information may break output formatting.
    """


def pytest_runtest_logreport(self, report):
    """Process a test setup/call/teardown report relating to the respective phase of executing a test.

    Hook changed to define SPECIFICATION like output format. This hook will overwrite also VERBOSE option.
    """
    res = self.config.hook.pytest_report_teststatus(report=report)
    cat, letter, word = res
    self.stats.setdefault(cat, []).append(report)
    if not letter and not word:
        return
    if not _is_nodeid_has_test(report.nodeid):
        return
    test_path = _get_test_path(report.nodeid)
    if test_path != self.currentfspath:
        self.currentfspath = test_path
        _print_class_information(self)
    if not isinstance(word, tuple):
        test_name = _get_test_name(report.nodeid)
        markup, test_status = _format_results(report)
        _print_test_result(self, test_name, test_status, markup)


def _is_nodeid_has_test(nodeid):
    if len(nodeid.split("::")) > 2:
        return True
    return False


def _get_test_path(nodeid):
    return nodeid.rsplit("::", 1)[0]


def _print_class_information(self):
    if hasattr(self, '_first_triggered'):
        self._tw.line()
    self._tw.line()
    self._tw.write(self.currentfspath)
    self._first_triggered = True


def _get_test_name(nodeid):
    test_name = nodeid.split("::")[2][5:].replace("_", " ").capitalize()
    if test_name[:1] is ' ':
        test_name_parts = test_name.split('  ')
        if len(test_name_parts) == 1:
            return test_name.strip().capitalize()
        return 'The ({}) {}'.format(test_name_parts[0][1:].replace(' ', '_'), test_name_parts[1])
    return test_name


def _format_results(report):
    if report.passed:
        return {'green': True}, '[PASS]  '
    elif report.failed:
        return {'red': True}, '[FAIL]  '
    elif report.skipped:
        return {'yellow': True}, '[SKIP]  '


def _print_test_result(self, test_name, test_status, markup):
    self._tw.line()
    self._tw.write("    {}{}".format(test_status, test_name), **markup)
