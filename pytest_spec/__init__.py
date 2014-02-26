# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""


def pytest_runtest_logstart(self, nodeid, location):
    """ Responsible for ??? """


def pytest_runtest_logreport(self, report):
    """ Responsible for report format """
    res = self.config.hook.pytest_report_teststatus(report=report)
    cat, letter, word = res
    self.stats.setdefault(cat, []).append(report)
    self._tests_ran = True
    if not letter and not word:
        return
    if self.verbosity > 0:
        return
    testname = report.nodeid.split("::")
    if len(testname) <= 2:
        return
    fspath = report.nodeid.rsplit("::", 1)[0]
    if fspath != self.currentfspath:
        self.currentfspath = fspath
        self._tw.line()
        if hasattr(self, "_first_fspath"):
            self._tw.line()
        self._first_fspath = True
        self._tw.write(fspath)
    if isinstance(word, tuple):
        word, markup = word
    else:
        if report.passed:
            markup = {'green': True}
        elif report.failed:
            markup = {'red': True}
        elif report.skipped:
            markup = {'yellow': True}
    test_status = None
    if 'green' in markup:
        test_status = '[PASS]  '
    elif 'red' in markup:
        test_status = '[FAIL]  '
    elif 'yellow' in markup:
        test_status = '[SKIP]  '
    self._tw.line()
    if len(testname) > 2:
        testname = testname[2][5:].replace("_", " ").capitalize()
        self._tw.write("    {}{}".format(test_status, testname), **markup)


#------------- MONKEY PATCH OF EXECUTION REPORT ---------------#
import imp
import _pytest
_pytest.terminal.TerminalReporter.pytest_runtest_logstart = pytest_runtest_logstart
_pytest.terminal.TerminalReporter.pytest_runtest_logreport = pytest_runtest_logreport
imp.reload(_pytest)
