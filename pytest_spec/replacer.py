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
    if not letter and not word:
        return
    if self.verbosity > 0:
        return
    if not is_nodeid_has_test(report.nodeid):
        return
    test_path = get_test_path(report.nodeid)
    if test_path != self.currentfspath:
        self.currentfspath = test_path
        print_class_information(self)
    if not isinstance(word, tuple):
        test_name = get_test_name(report.nodeid)
        markup, test_status = format_results(report)
        print_test_result(self, test_name, test_status, markup)


def is_nodeid_has_test(nodeid):
    if len(nodeid.split("::")) > 2:
        return True
    return False


def get_test_path(nodeid):
    return nodeid.rsplit("::", 1)[0]


def print_class_information(self):
    self._tw.line()
    self._tw.line()
    self._tw.write(self.currentfspath)


def get_test_name(nodeid):
    return nodeid.split("::")[2][5:].replace("_", " ").capitalize()


def format_results(report):
    if report.passed:
        return {'green': True}, '[PASS]  '
    elif report.failed:
        return {'red': True}, '[FAIL]  '
    elif report.skipped:
        return {'yellow': True}, '[SKIP]  '


def print_test_result(self, test_name, test_status, markup):
    self._tw.line()
    self._tw.write("    {}{}".format(test_status, test_name), **markup)
