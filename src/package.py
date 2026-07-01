from pathlib import Path

import dnf
import os

import logger


dnf = dnf.Base()
dnf.read_all_repos()
dnf.fill_sack()

from rpmlint.lint import Lint

class Specfile:
    def __init__(self,path : str | None) -> None:
        if path is None or not os.path.isfile(path):
            raise FileNotFoundError
        self.path: str = path
        self._linter: Lint = Lint(options={
            'rpmfile': [],
            # Has to be empty, otherwise it will exit, we want to use the output with validate_file
            'checks': "",
            'config': [],
            'explain': [],
            'ignore_unused_rpmlintrc': False,
            'installed': [],
            'permissive': False,
            'print_config': False,
            'profile': False,
            'rpmlintrc': [],
            'strict': False,
            'time_report': False,
            'verbose': False
        })

    def lint(self) -> None:
        self._linter.validate_file(Path(self.path),True)
        
        logger.Notice(repr(self._linter.output.results),"Lint results")
    # def installBuildDeps(self) -> None:
        # spec.
        # dnf.install_specs([""])
        # dnf.resolve()



