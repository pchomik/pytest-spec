# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""


def pytest_runtest_logstart(self, nodeid, location):
    """ Responsible for ??? """


def pytest_runtest_logreport(self, report):
    """ Responsible for report format """
    test_status = None
    res = self.config.hook.pytest_report_teststatus(report=report)
    cat, letter, word = res
    self.stats.setdefault(cat, []).append(report)
    if not letter and not word:
        return
    if self.verbosity > 0:
        return
    if not is_nodeid_has_test(report.nodeid):
        return
    fspath = get_test_path(report.nodeid)
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
        markup, test_status = format_results(report)
    self._tw.line()
    self._tw.write("    {}{}".format(test_status, get_test_name(report.nodeid)), **markup)


def is_nodeid_has_test(nodeid):
    if len(nodeid.split("::")) > 2:
        return True
    return False


def get_test_path(nodeid):
    return nodeid.rsplit("::", 1)[0]


def get_test_name(nodeid):
    return nodeid.split("::")[2][5:].replace("_", " ").capitalize()


def format_results(report):
    if report.passed:
        return {'green': True}, '[PASS]  '
    elif report.failed:
        return {'red': True}, '[FAIL]  '
    elif report.skipped:
        return {'yellow': True}, '[SKIP]  '