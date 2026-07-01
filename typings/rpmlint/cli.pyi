
from typing import Any, TypedDict


class LintOptions(TypedDict,total=True):

    """
    Options for Lint. Manually created stub from cli.py process_lint_args
    """

    rpmfile: list[str]
    """
    Files to be validated by rpmlint
    """

    strict: bool
    """
    Treat all messages as errors. Mutually exclusive with permissive.
    """

    permissive: bool
    """
    Treat individual errors as non-fatal. Mutually exclusive with strict.
    """

    config: list[str]
    """
    Load up additional configuration data from specified path (file or directory with *.toml files)
    """

    explain: list[int]
    """
    Provide detailed explanation for one specific message id
    """

    rpmlintrc: list[str]
    """
    Load up specified rpmlintrc file (may be repeated)
    """

    verbose: bool
    """
    Provide detailed explanations where available
    """

    print_config: bool
    """
    Print the settings that are in effect when using the rpmlint
    """

    installed: list[str]
    """
    Installed packages to be validated by rpmlint
    """

    time_report: bool
    """
    Print time report for run checks
    """

    profile: bool
    """
    Print cProfile report
    """

    ignore_unused_rpmlintrc: bool
    """
    Do not report "unused_rpmlintrc_filter" errors
    """

    checks: str
    """
    Debugging option that enables only selected checks (separated by comma)
    """



__copyright__ : str = ...

def process_diff_args(argv: list[str]) -> dict[str, Any]:
    """
    Process the passed arguments and return the result
    :param argv: passed arguments
    """
    ...

def process_lint_args(argv: list[str]) -> LintOptions:
    """
    Process the passed arguments and return the result
    :param argv: passed arguments
    """
    ...

def lint():
    """
    Main wrapper for lint command processing
    """
    ...

def diff():
    """
    Main wrapper for diff command processing
    """
    ...

