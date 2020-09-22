# -*- coding: utf-8 -*-
"""Module contains method that will be replaced by the plugin.

:author: Pawel Chomicki
"""

import os
import re


def pytest_runtest_logstart(self, nodeid, location):
    """Signal the start of running a single test item.

    Hook has to be disabled because additional information may break output
    formatting.
    """
    pass


def pytest_collection_modifyitems(session, config, items):
    def get_module_name(f):
        return f.listchain()[1].name

    def get_nodeid(f):
        return "::".join(f.nodeid.split('::')[:-1])

    items.sort(key=get_nodeid)
    items.sort(key=get_module_name)
    return items


def get_report_scopes(report):
    """
    Returns a list of the report's nested scopes, excluding the module.

    >>> report = lambda s: s
    >>> report.nodeid = (
        "specs/user.py::describe_a_user::"
        "describe_email_address::cannot_be_hotmail"
    )
    >>> get_report_scopes(report)
    ['describe_a_user', 'describe_email_address']
    """
    return [i for i in report.nodeid.split('::')[1:-1] if i != '()']


def pytest_runtest_logreport(self, report):
    """
    Process a test setup/call/teardown report relating to the respective phase
    of executing a test.

    Hook changed to define SPECIFICATION like output format. This hook will
    overwrite also VERBOSE option.
    """
    self.previous_scopes = getattr(self, 'previous_scopes', [])
    self.current_scopes = get_report_scopes(report)
    indent = self.config.getini('spec_indent')

    res = self.config.hook.pytest_report_teststatus(report=report, config=self.config)
    cat, letter, word = res
    self.stats.setdefault(cat, []).append(report)
    if not letter and not word:
        return
    if not _is_nodeid_has_test(report.nodeid):
        return
    test_path = _get_test_path(report.nodeid, self.config.getini('spec_header_format'))
    if test_path != self.currentfspath:
        self.currentfspath = test_path
        _print_description(self)

    scope_ind = 0
    for msg in self.current_scopes:
        if msg not in self.previous_scopes:
            msg = [indent * scope_ind + prettify_description(msg)]
            msg = "\n".join(msg)
            if msg:
                _print_description(self, msg)
        scope_ind += 1
    self.previous_scopes = self.current_scopes

    if not isinstance(word, tuple):
        test_name = _get_test_name(report.nodeid)
        markup, test_status = _format_results(report, self.config)
        depth = len(self.current_scopes)
        _print_test_result(self, test_name, test_status, markup, depth)


def _is_nodeid_has_test(nodeid):
    if len(nodeid.split("::")) >= 2:
        return True
    return False


def prettify(string):
    return _capitalize_first_letter(
        _replace_underscores(
            _remove_test_container_prefix(
                _remove_file_extension(string))))


def prettify_test(string):
    return prettify(_remove_test_prefix(string))


def prettify_description(string):
    return prettify(_append_colon(_remove_test_container_prefix(string)))


def _get_test_path(nodeid, header):
    levels = nodeid.split("::")

    module_path = levels[0]
    module_name = os.path.split(levels[0])[1]

    if len(levels) > 2:
        class_name = levels[1]
        test_case = prettify(class_name)
    else:
        class_name = ''
        test_case = prettify(module_name)

    return header.format(
        path=levels[0],
        module_name=module_name,
        module_path=module_path,
        class_name=class_name,
        test_case=test_case
    )


def _print_description(self, msg=None):
    if msg is None:
        msg = self.currentfspath
    if hasattr(self, '_first_triggered'):
        self._tw.line()
    self._tw.line()
    self._tw.write(msg)
    self._first_triggered = True


def _remove_test_container_prefix(nodeid):
    return re.sub("^(Test)|(describe)", "", nodeid)


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


def _append_colon(string):
    return "{}:".format(string)


def _get_test_name(nodeid):
    test_name = prettify_test(_remove_module_name(nodeid))
    if test_name[:1] == ' ':
        test_name_parts = test_name.split('  ')
        if len(test_name_parts) == 1:
            return test_name.strip().capitalize()
        return 'The ({0}) {1}'.format(test_name_parts[0][1:].replace(' ', '_'), test_name_parts[1])
    return test_name


def _format_results(report, config):
    success_indicator = config.getini('spec_success_indicator')
    failure_indicator = config.getini('spec_failure_indicator')
    skipped_indicator = config.getini('spec_skipped_indicator')
    if report.passed:
        return {'green': True}, success_indicator
    elif report.failed:
        return {'red': True}, failure_indicator
    elif report.skipped:
        return {'yellow': True}, skipped_indicator


def _print_test_result(self, test_name, test_status, markup, depth):
    indent = self.config.getini('spec_indent')
    self._tw.line()
    self._tw.write(
        indent * depth + self.config.getini('spec_test_format').format(
            result=test_status, name=test_name
        ), **markup
    )
