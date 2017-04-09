# -*- coding: utf-8 -*-
"""Module contains method that will be replaced by the plugin.

:author: Pawel Chomicki
"""

import os
import re
import pdb

from .reader import Reader
from .cache import Cache


P_REGEX = re.compile(r'({p\d})')     # P_REGEX - findall will work


def pytest_runtest_logstart(self, nodeid, location):
    """Signal the start of running a single test item.

    Hook has to be disabled because additional information may break output formatting.
    """


def pytest_runtest_logreport(self, report):
    """Process a test setup/call/teardown report relating to the respective phase of executing a test.

    Hook changed to define SPECIFICATION like output format. This hook will overwrite also VERBOSE option.
    """
    _read_test_format(report)
    res = self.config.hook.pytest_report_teststatus(report=report)
    cat, letter, word = res
    self.stats.setdefault(cat, []).append(report)
    if not letter and not word:
        return
    if not _is_nodeid_has_test(report.nodeid):
        return
    test_path = _get_test_path(report.nodeid, self.config.getini('spec_header_format'))
    if test_path != self.currentfspath:
        self.currentfspath = test_path
        _print_class_information(self)
    if not isinstance(word, tuple):
        test_name = _get_test_name(report.nodeid)
        markup, test_status = _format_results(report)
        _print_test_result(self, report, test_name, test_status, markup)


def _read_test_format(report):
    cache = Cache()
    test_spec_format = cache.get(report.fspath) or \
        Reader().read_spec_test_format(report.fspath) or \
        cache.default
    cache.put(report.fspath, test_spec_format)


def _is_nodeid_has_test(nodeid):
    if len(nodeid.split("::")) >= 2:
        return True
    return False


def _get_test_path(nodeid, header):
    levels = nodeid.split("::")

    if len(levels) > 2:
        class_name = levels[1]
        test_case = _split_words(_remove_class_prefix(class_name))
    else:
        module_name = os.path.split(levels[0])[1]
        class_name = ''
        test_case = _capitalize_first_letter(_replace_underscores(_remove_test_prefix(_remove_file_extension(module_name))))

    return header.format(path=levels[0], class_name=class_name, test_case=test_case)


def _print_class_information(self):
    if hasattr(self, '_first_triggered'):
        self._tw.line()
    self._tw.line()
    self._tw.write(self.currentfspath)
    self._first_triggered = True


def _remove_class_prefix(nodeid):
    return re.sub("^Test", "", nodeid)


def _split_words(nodeid):
    return re.sub(r"([A-Z])", r" \1", nodeid).strip()


def _remove_file_extension(nodeid):
    return os.path.splitext(nodeid)[0]


def _remove_module_name(nodeid):
    return nodeid.rsplit("::", 1)[1]


def _remove_test_prefix(nodeid):
    return re.sub("^test_+", "", nodeid)


def _replace_underscores(nodeid):
    return nodeid.replace("__", " ").strip().replace("_", " ").strip()


def _capitalize_first_letter(s):
    return s[:1].capitalize() + s[1:]


def _get_test_name(nodeid):
    test_name = _capitalize_first_letter(_replace_underscores(_remove_test_prefix(_remove_module_name(nodeid))))
    if test_name[:1] is ' ':
        test_name_parts = test_name.split('  ')
        if len(test_name_parts) == 1:
            return test_name.strip().capitalize()
        return 'The ({0}) {1}'.format(test_name_parts[0][1:].replace(' ', '_'), test_name_parts[1])
    return test_name


def _format_results(report):
    if report.passed:
        return {'green': True}, 'PASS'
    elif report.failed:
        return {'red': True}, 'FAIL'
    elif report.skipped:
        return {'yellow': True}, 'SKIP'


def _print_test_result(self, report, test_name, test_status, markup):
    test_format = Cache().get(report.fspath)
    params_count = len(P_REGEX.findall(test_format))
    params = []
    if params_count > 0:
        result = test_name.strip().split('[')
        if len(result) > 1:
            test_name, params = result
            params = _clean_params(params)
    format_params = {
        'result': test_status,
        'name': test_name
    }
    _add_formats_for_params(params, params_count, format_params)
    self._tw.line()
    self._tw.write("    "+test_format.format(**format_params), **markup)


def _clean_params(params):
    params = params[:-1]
    params = params.split(',')
    params = [each.strip() for each in params]
    return params


def _add_formats_for_params(params, params_count, format_params):
    for index in range(params_count):
        if index < len(params):
            format_params['p{}'.format(index)] = params[index]
        else:
            format_params['p{}'.format(index)] = ''
