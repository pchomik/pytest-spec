"""Module contains command line option definition and logic needed to enable new formatting.

:author: Pawel Chomicki
"""

from typing import Any

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Item
from _pytest.runner import CallInfo

from pytest_spec.replacer import logstart_replacer, modifyitems_replacer, report_replacer


def pytest_addoption(parser: Parser) -> None:
    """Adds command line option to enable spec format."""
    group = parser.getgroup("general")
    group.addoption(
        "--spec",
        action="store_true",
        dest="spec",
        help="Print test result in specification format",
    )

    # register config options
    parser.addini(
        "spec_header_format",
        default="{module_path}:",
        help="The format of the test headers when using the spec plugin",
    )
    parser.addini(
        "spec_container_format",
        default="{sentence}:",
        help="The format of the test container when using the spec plugin",
    )
    parser.addini(
        "spec_test_format",
        default="{result} {name}",
        help="The format of the test results when using the spec plugin",
    )
    parser.addini(
        "spec_override_with_docstring",
        default=False,
        help="Overrides variables in the container and test result formats with the first line of the docstring if it exists",
    )
    parser.addini(
        "spec_success_indicator",
        default="✓",
        help="The indicator displayed when a test passes",
    )
    parser.addini(
        "spec_failure_indicator",
        default="✗",
        help="The indicator displayed when a test fails",
    )
    parser.addini(
        "spec_skipped_indicator",
        default="»",
        help="The indicator displayed when a test is skipped",
    )
    parser.addini(
        "spec_indent",
        default="  ",
        help="The string used for indentation in the spec output",
    )
    parser.addini(
        "spec_ignore",
        default="",
        help="The comma-separated list of strings used to ignore tests in the spec output e.g. FLAKE8",
    )


def pytest_configure(config: Config) -> None:
    """Enables spec format if command line option is present."""
    if getattr(config.option, "spec", 0) and not getattr(config.option, "quiet", 0) and not getattr(config.option, "verbose", 0):
        import importlib

        import _pytest

        _pytest.terminal.TerminalReporter.pytest_runtest_logstart = logstart_replacer  # type: ignore
        _pytest.terminal.TerminalReporter.pytest_runtest_logreport = report_replacer  # type: ignore
        _pytest.terminal.TerminalReporter.pytest_collection_modifyitems = modifyitems_replacer  # type: ignore
        importlib.reload(_pytest)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo) -> Any:
    """Adds docstring summary to the report."""
    outcome = yield
    report = outcome.get_result()
    if hasattr(item, "obj") and item.obj.__doc__:
        report.docstring_summary = str(item.obj.__doc__).lstrip().split("\n")  # type: ignore
    else:
        report.docstring_summary = []

    # describe_hierarchy = item.get_describe_function_heirarchy() if hasattr(item, "get_describe_function_heirarchy") else None
    # if describe_hierarchy is not None:
    #     report.describe_hierarchy = [{"name": f.__name__, "doc": f.__doc__ or ""} for f in describe_hierarchy]
    # else:
    #     report.describe_hierarchy = _get_describe_hierarchy_by_duck_typing(item)
    report.describe_hierarchy = _get_describe_hierarchy_by_duck_typing(item)


def _get_describe_hierarchy_by_duck_typing(item: Item) -> list[dict[str, str]]:
    hierarchy = []
    parent = item.parent
    while parent is not None:
        class_name = parent.__class__.__name__
        funcobj = getattr(parent, "funcobj", None)

        if class_name == "DescribeBlock" and callable(funcobj):
            hierarchy.append({"name": funcobj.__name__, "doc": funcobj.__doc__ or ""})

        parent = parent.parent
    return hierarchy
