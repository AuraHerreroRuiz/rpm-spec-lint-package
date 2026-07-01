from pathlib import Path
from typing import Literal

from rpmlint.cli import LintOptions
from rpmlint.filter import Filter
type ReturnCodes = Literal[0, 66, 65, 64]

class Lint:
    """
    Generic object handling the basic rpmlint operations
    """
    output : Filter

    def __init__(self, options : LintOptions) -> None:
        ...

    def run(self) -> ReturnCodes:
        ...

    def validate_installed_packages(self, packages) -> None:
        ...

    def validate_files(self, files: list[Path]) -> None:
        """
        Run all the check for passed file list
        """
        ...

    def validate_file(self, pname: Path, is_last: bool) -> None:
        ...

    def run_checks(self, pkg, is_last: bool) -> None:
        ...

    def print_config(self) -> None:
        """
        Just output the current configuration
        """
        ...

    def print_explanation(self, messages, config) -> None:
        """
        Print out detailed explanation for the specified messages
        """
        ...

    def load_checks(self) -> None:
        """
        Load all checks based on the config, skipping those already loaded
        SingletonTM
        """
        ...

    def reset_checks(self) -> None:
        """
        Reset all check objects to set to the default state
        """
        ...

    def load_check(self, name) -> Any:
        """Load a (check) module by its name, unless it is already loaded."""
        ...



